"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
from servalcat.utils import logger
import os
import io
import gemmi
import string
import random
import numpy

default_proton_scale = 1.13 # scale of X-proton distance to X-H(e) distance

def decide_new_mod_id(mod_id, mods):
    # Refmac only allows up to 8 characters
    letters = string.digits + string.ascii_lowercase
    if len(mod_id) < 8:
        for l in letters:
            new_id = "{}{}{}".format(mod_id, "" if len(mod_id)==7 else "-", l)
            if new_id not in mods:
                return new_id

    # give up keeping original name
    while True: # XXX risk of infinite loop.. less likely though
        new_id = "mod" + "".join([random.choice(letters) for _ in range(4)])
        if new_id not in mods:
            return new_id
# decide_new_mod_id()

def rename_cif_modification_if_necessary(doc, known_ids):
    # FIXME Problematic if other file refers to modification that is renamed in this function - but how can we know?
    trans = {}
    for b in doc:
        for row in b.find("_chem_mod.", ["id"]):
            mod_id = row.str(0)
            if mod_id in known_ids:
                new_id = decide_new_mod_id(mod_id, known_ids)
                trans[mod_id] = new_id
                row[0] = new_id # modify id
                logger.writeln("INFO:: renaming modification id {} to {}".format(mod_id, new_id))

    # modify ids in mod_* blocks
    for mod_id in trans:
        b = doc.find_block("mod_{}".format(mod_id))
        if not b: # should raise error?
            logger.writeln("WARNING:: inconsistent mod description for {}".format(mod_id))
            continue
        b.name = "mod_{}".format(trans[mod_id]) # modify name
        for item in b:
            for tag in item.loop.tags:
                if tag.endswith(".mod_id"):
                    for row in b.find(tag[:tag.rindex(".")+1], ["mod_id"]):
                        row[0] = trans[mod_id]

    # Update mod id in links
    if trans:
        for b in doc:
            for row in b.find("_chem_link.", ["mod_id_1", "mod_id_2"]):
                for i in range(2):
                    if row.str(i) in trans:
                        row[i] = trans[row.str(i)]

    return trans
# rename_cif_modification_if_necessary()

def load_monomer_library(st, monomer_dir=None, cif_files=None, stop_for_unknowns=False,
                         ignore_monomer_dir=False):
    resnames = st[0].get_all_residue_names()

    if monomer_dir is None and not ignore_monomer_dir:
        if "CLIBD_MON" not in os.environ:
            logger.error("WARNING: CLIBD_MON is not set")
        else:
            monomer_dir = os.environ["CLIBD_MON"]

    if cif_files is None:
        cif_files = []
        
    if monomer_dir and not ignore_monomer_dir:
        if not os.path.isdir(monomer_dir):
            logger.error("ERROR: not a directory: {}".format(monomer_dir))
            return

        logger.writeln("Reading monomers from {}".format(monomer_dir))
        monlib = gemmi.read_monomer_lib(monomer_dir, resnames, ignore_missing=True)
    else:
        monlib = gemmi.MonLib()

    for f in cif_files:
        logger.writeln("Reading monomer: {}".format(f))
        doc = gemmi.cif.read(f)
        for b in doc:
            atom_id_list = b.find_values("_chem_comp_atom.atom_id")
            if atom_id_list:
                name = b.name.replace("comp_", "")
                if name in monlib.monomers:
                    logger.writeln("WARNING:: updating monomer {} using {}".format(name, f))
                    del monlib.monomers[name]

                # Check if bond length values are included
                # This is to fail if cif file is e.g. from PDB website
                if len(atom_id_list) > 1 and not b.find_values("_chem_comp_bond.value_dist"):
                    raise RuntimeError("{} does not contain bond length value for {}. You need to generate restraints (e.g. using acedrg).".format(f, name))
                    
            for row in b.find("_chem_link.", ["id"]):
                link_id = row.str(0)
                if link_id in monlib.links:
                    logger.writeln("WARNING:: updating link {} using {}".format(link_id, f))
                    del monlib.links[link_id]

        # If modification id is duplicated, need to rename
        rename_cif_modification_if_necessary(doc, monlib.modifications)
        monlib.read_monomer_doc(doc)
        for b in doc:
            for row in b.find("_chem_comp.", ["id", "group"]):
                if row.str(0) in monlib.monomers:
                    monlib.monomers[row.str(0)].set_group(row.str(1))

    not_loaded = set(resnames).difference(monlib.monomers)
    if not_loaded:
        logger.writeln("WARNING: monomers not loaded: {}".format(" ".join(not_loaded)))
        
    logger.writeln("Monomer library loaded: {} monomers, {} links, {} modifications".format(len(monlib.monomers),
                                                                                          len(monlib.links),
                                                                                          len(monlib.modifications)))
    logger.writeln("       loaded monomers: {}".format(" ".join([x for x in monlib.monomers])))
    logger.writeln("")

    logger.writeln("Checking if unknown atoms exist..")

    unknown_cc = set()
    for chain in st[0]: unknown_cc.update(res.name for res in chain if res.name not in monlib.monomers)
    if unknown_cc:
        if stop_for_unknowns:
            raise RuntimeError("Provide restraint cif file(s) for {}".format(",".join(unknown_cc)))
        else:
            logger.writeln("WARNING: ad-hoc restraints will be generated for {}".format(",".join(unknown_cc)))
            logger.writeln("         it is strongly recommended to generate them using AceDRG.")
    
    return monlib
# load_monomer_library()

def prepare_topology(st, monlib, h_change, ignore_unknown_links=False, raise_error=True, check_hydrogen=False,
                     use_cispeps=False):
    # these checks can be done after sorting links
    logger.writeln("Creating restraints..")
    sio = io.StringIO()
    topo = gemmi.prepare_topology(st, monlib, h_change=h_change, warnings=sio, reorder=False,
                                  ignore_unknown_links=ignore_unknown_links, use_cispeps=use_cispeps)
    for l in sio.getvalue().splitlines(): logger.writeln(" " + l)
    unknown_cc = set()
    link_related = set()
    nan_hydr = set()
    for cinfo in topo.chain_infos:
        for rinfo in cinfo.res_infos:
            cc_org = monlib.monomers[rinfo.res.name] if rinfo.res.name in monlib.monomers else None
            for ia in reversed(range(len(rinfo.res))):
                atom = rinfo.res[ia]
                atom_str = "{}/{} {}/{}".format(cinfo.chain_ref.name, rinfo.res.name, rinfo.res.seqid, atom.name)
                cc = rinfo.get_final_chemcomp(atom.altloc)
                if not cc.find_atom(atom.name):
                    # warning message should have already been given by gemmi
                    if cc_org and cc_org.find_atom(atom.name):
                        if check_hydrogen or not atom.is_hydrogen():
                            link_related.add(rinfo.res.name)
                    else:
                        if check_hydrogen or not atom.is_hydrogen():
                            unknown_cc.add(rinfo.res.name)
                
                if atom.is_hydrogen() and atom.calc_flag == gemmi.CalcFlag.Dummy:
                    logger.writeln(" Warning: hydrogen {} could not be added - Check dictionary".format(atom_str))
                    unknown_cc.add(rinfo.res.name)
                elif any(numpy.isnan(atom.pos.tolist())): # TODO add NaN test before prepare_toplogy
                    logger.writeln(" Warning: {} position NaN!".format(atom_str))
                    nan_hydr.add(rinfo.res.name)

    if raise_error and (unknown_cc or link_related):
        msgs = []
        if unknown_cc: msgs.append("restraint cif file(s) for {}".format(",".join(unknown_cc)))
        if link_related: msgs.append("proper link cif file(s) for {} or check your model".format(",".join(link_related)))
        raise RuntimeError("Provide {}".format(" and ".join(msgs)))
    if raise_error and nan_hydr:
        raise RuntimeError("Some hydrogen positions became NaN. The geometry of your model may be of low quality. Consider not adding hydrogen")
    if not use_cispeps:
        topo.set_cispeps_in_structure(st)
    return topo
# prepare_topology()

def check_monlib_support_nucleus_distances(monlib, resnames):
    good = True
    nucl_not_found = []
    for resn in resnames:
        if resn not in monlib.monomers:
            logger.error("ERROR: monomer information of {} not loaded".format(resn))
            good = False
        else:
            mon = monlib.monomers[resn]
            no_nuc = False
            for bond in mon.rt.bonds:
                is_h = (mon.get_atom(bond.id1.atom).is_hydrogen(), mon.get_atom(bond.id2.atom).is_hydrogen())
                if any(is_h) and bond.value_nucleus != bond.value_nucleus:
                    no_nuc = True
                    break
            if no_nuc:
                nucl_not_found.append(resn)
                good = False

    if nucl_not_found:
        logger.writeln("WARNING: nucleus distance is not found for: {}".format(" ".join(nucl_not_found)))
        logger.writeln("         default scale ({}) is used for nucleus distances.".format(default_proton_scale))
    return good
# check_monlib_support_nucleus_distances()

def find_and_fix_links(st, monlib, bond_margin=1.3, find_metal_links=True, add_found=True, find_symmetry_related=True):
    """
    Identify link ids for st.connections and find new links
    This is required for correctly recognizing link in gemmi.prepare_topology
    Note that it ignores segment IDs
    FIXME it assumes only one bond exists in a link. It may not be the case in future.
    """
    from servalcat.utils import model

    logger.writeln("Checking links defined in the model")
    for con in st.connections:
        if con.type == gemmi.ConnectionType.Hydrog: continue
        cra1, cra2 = st[0].find_cra(con.partner1, ignore_segment=True), st[0].find_cra(con.partner2, ignore_segment=True)
        if None in (cra1.atom, cra2.atom):
            logger.writeln(" WARNING: atom(s) not found for link: id= {} atom1= {} atom2= {}".format(con.link_id, con.partner1, con.partner2))
            continue
        if con.asu == gemmi.Asu.Different:
            nimage = st.cell.find_nearest_image(cra1.atom.pos, cra2.atom.pos, con.asu)
            image_idx = nimage.sym_idx
            dist = nimage.dist()
        else:
            image_idx = 0
            dist = cra1.atom.pos.dist(cra2.atom.pos)
        atoms_str = "atom1= {} atom2= {} image= {}".format(cra1, cra2, image_idx)
        if con.link_id:
            link = monlib.get_link(con.link_id)
            inv = False
            if link is None:
                logger.writeln(" WARNING: link {} not found in the library. Please provide link dictionary.".format(con.link_id))
                continue
            else:
                match, _, _ = monlib.test_link(link, cra1.residue.name, cra1.atom.name, cra2.residue.name, cra2.atom.name)
                if not match and monlib.test_link(link, cra2.residue.name, cra2.atom.name, cra1.residue.name, cra1.atom.name)[0]:
                    match = True
                    inv = True
                if not match:
                    logger.writeln(" WARNING: link id and atoms mismatch: id= {} {}".format(link.id, atoms_str))
                    continue
        else:
            link, inv, _, _ = monlib.match_link(cra1.residue, cra1.atom.name, cra1.atom.altloc,
                                                cra2.residue, cra2.atom.name, cra2.atom.altloc)
            if link:
                con.link_id = link.id
            else:
                ideal_dist = monlib.find_ideal_distance(cra1, cra2)
                logger.writeln(" Link unidentified (simple bond will be used): {} dist= {:.2f} ideal= {:.2f}".format(atoms_str,
                                                                                                                     dist,
                                                                                                                     ideal_dist))
                continue
        if link:
            logger.writeln(" Link confirmed: id= {} {} dist= {:.2f} ideal= {:.2f}".format(link.id,
                                                                                          atoms_str,
                                                                                          dist,
                                                                                          link.rt.bonds[0].value))
            if inv:
                con.partner1 = model.cra_to_atomaddress(cra2)
                con.partner2 = model.cra_to_atomaddress(cra1)
    if len(st.connections) == 0:
        logger.writeln(" no links defined in the model")

    logger.writeln("Finding new links (will {} added)".format("be" if add_found else "not be"))
    ns = gemmi.NeighborSearch(st[0], st.cell, 5.).populate()
    cs = gemmi.ContactSearch(3.1)
    cs.ignore = gemmi.ContactSearch.Ignore.AdjacentResidues # may miss polymer links not contiguous in a chain?
    results = cs.find_contacts(ns)
    onsb = set(gemmi.Element(x) for x in "ONSB")
    n_found = 0
    for r in results:
        if not find_symmetry_related and r.image_idx != 0: continue
        if st.find_connection_by_cra(r.partner1, r.partner2): continue
        link, inv, _, _ = monlib.match_link(r.partner1.residue, r.partner1.atom.name, r.partner1.atom.altloc,
                                            r.partner2.residue, r.partner2.atom.name, r.partner2.atom.altloc,
                                            (r.dist / 1.4)**2)
        if inv:
            cra1, cra2 = r.partner2, r.partner1
        else:
            cra1, cra2 = r.partner1, r.partner2
        atoms_str = "atom1= {} atom2= {} image= {}".format(cra1, cra2, r.image_idx)
        if link:
            if r.dist > link.rt.bonds[0].value * bond_margin: continue
            logger.writeln(" New link found: id= {} {} dist= {:.2f} ideal= {:.2f}".format(link.id,
                                                                                          atoms_str,
                                                                                          r.dist,
                                                                                          link.rt.bonds[0].value))
        elif find_metal_links:
            # link only metal - O/N/S/B
            if r.partner1.atom.element.is_metal == r.partner2.atom.element.is_metal: continue
            if not r.partner1.atom.element in onsb and not r.partner2.atom.element in onsb: continue
            ideal_dist = monlib.find_ideal_distance(r.partner1, r.partner2)
            if r.dist > ideal_dist * bond_margin: continue
            logger.writeln(" Metal link found: {} dist= {:.2f} ideal= {:.2f}".format(atoms_str,
                                                                                     r.dist, ideal_dist))
        n_found += 1
        if not add_found: continue
        con = gemmi.Connection()
        con.name = "added{}".format(n_found)
        if link:
            con.link_id = link.id
            con.type = gemmi.ConnectionType.Covale
        else:
            con.type = gemmi.ConnectionType.MetalC
        con.asu = gemmi.Asu.Same if r.image_idx == 0 else gemmi.Asu.Different
        con.partner1 = model.cra_to_atomaddress(cra1)
        con.partner2 = model.cra_to_atomaddress(cra2)
        con.reported_distance = r.dist
        st.connections.append(con)
    if n_found == 0:
        logger.writeln(" no links found")
# find_and_fix_links()

def add_hydrogens(st, monlib, pos="elec"):
    assert pos in ("elec", "nucl")
    # perhaps this should be done outside..
    st.entities.clear()
    st.setup_entities()

    topo = prepare_topology(st, monlib, h_change=gemmi.HydrogenChange.ReAddButWater, ignore_unknown_links=True)
    
    if pos == "nucl":
        logger.writeln("Generating hydrogens at nucleus positions")
        resnames = st[0].get_all_residue_names()
        check_monlib_support_nucleus_distances(monlib, resnames)
        topo.adjust_hydrogen_distances(gemmi.Restraints.DistanceOf.Nucleus, default_scale=default_proton_scale)
    else:
        logger.writeln("Generating hydrogens at electron positions")
# add_hydrogens()
