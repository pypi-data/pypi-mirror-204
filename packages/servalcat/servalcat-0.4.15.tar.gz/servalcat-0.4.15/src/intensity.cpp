// Author: "Keitaro Yamashita, Garib N. Murshudov"
// MRC Laboratory of Molecular Biology

#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <gemmi/bessel.hpp>
#include "math.hpp"
namespace py = pybind11;
using namespace servalcat;

// for MLI
double f1_orig2(double x, double z, double to, double tf, double sig1, int c) {
  // z = 2k+1
  const double x2 = x * x;
  const double ret = 0.5 * x2 * x2 - to * x2 - z * std::log(x);
  if (tf == 0.) return ret;
  const double X = x * tf / sig1;
  const double log_ic0 = c == 1 ? gemmi::log_bessel_i0(2*X) : log_cosh(X);
  return ret - log_ic0;
}
double f1_orig2_der1(double x, double z, double to, double tf, double sig1, int c) {
  const double ret = 2 * x*x*x - 2 * to * x - z / x;
  if (tf == 0.) return ret;
  const double X = x * tf / sig1;
  const double m = fom(X, c);
  return ret - m * (3-c) * tf / sig1;
}
double f1_orig2_der2(double x, double z, double to, double tf, double sig1, int c) {
  const double x2 = x * x;
  const double ret = 6 * x2 - 2 * to + z / x2;
  if (tf == 0.) return ret;
  const double X = x * tf / sig1;
  const double m = fom(X, c);
  const double m_der = fom_der(m, X, c);
  return ret - (3-c)*(3-c) * tf*tf * m_der / (sig1*sig1);
}
double f1_exp2(double y, double z, double to, double tf, double sig1, int c) {
  // z = 2k+2
  const double e_y = std::exp(-y);
  const double exp2 = std::exp(2 * (y - e_y));
  const double ret = 0.5 * exp2*exp2 - to * exp2 - z * (y - e_y) - std::log(1 + e_y);
  if (tf == 0.) return ret;
  const double X = std::exp(y - e_y) * tf / sig1;
  const double log_ic0 = c == 1 ? gemmi::log_bessel_i0(2*X) : log_cosh(X);
  return ret - log_ic0;
}
double f1_exp2_der1(double y, double z, double to, double tf, double sig1, int c) {
  const double e_y = std::exp(-y);
  const double exp2 = std::exp(2 * (y - e_y));
  const double ret = (1 + e_y) * (2 * exp2*exp2 - 2 * to * exp2 - z) + e_y / (1 + e_y);
  if (tf == 0.) return ret;
  const double X = std::exp(y - e_y) * tf / sig1;
  const double m = fom(X, c);
  return ret - (1 + e_y) * ((3-c) * tf / sig1 * m * std::exp(y - e_y));
}
double f1_exp2_der2(double y, double z, double to, double tf, double sig1, int c) {
  const double e_y = std::exp(-y);
  const double exp2 = std::exp(2 * (y - e_y));
  const double ret = -e_y * (2 * exp2*exp2 - 2 * to * exp2 - z) + sq(1 + e_y) * (8 * sq(exp2) - 4 * to * exp2) - e_y / sq(1 + e_y);
  if (tf == 0.) return ret;
  const double X = std::exp(y - e_y) * tf / sig1;
  const double m = fom(X, c);
  const double m_der = tf == 0 ? 0 : fom_der(m, X, c);
  return ret + e_y * (3-c) * tf / sig1 * m * std::exp(y - e_y) - sq(1 + e_y) * ((3-c) * tf / sig1 * m * std::exp(y - e_y) - sq(3-c) * sq(tf / sig1) * m_der * exp2);
}
double find_root(double k, double to, double tf, double sig1, int c, double det, bool use_exp2) {
  if (tf == 0.) {
    if (use_exp2)
      return solve_y_minus_exp_minus_y(0.5 * std::log(0.5 * x_plus_sqrt_xsq_plus_y(to, 4 * k + 4)), 1e-2); // XXX may not be exact
    return det;
  }
  const double z = use_exp2 ? 2 * k + 2 : 2 * k + 1;
  auto fder1 = use_exp2 ? f1_exp2_der1 : f1_orig2_der1;
  auto fder2 = use_exp2 ? f1_exp2_der2 : f1_orig2_der2;
  double x0 = det, x1 = NAN;
  if (use_exp2) {
    const double X1 = (3-c) * tf * 0.5 / sig1 * std::sqrt(0.5 * x_plus_sqrt_xsq_plus_y(to, 4 * k + 3.5));
    const double m1 = fom(X1, c);
    x0 = solve_y_minus_exp_minus_y(0.5 * std::log(0.5 * x_plus_sqrt_xsq_plus_y(to, 4 * k + 4 * X1 * m1 + 3.5)), 1e-2);
    const double A = std::max(to, std::max((3-c) * tf / 4 / sig1, k + 1));
    x1 = solve_y_minus_exp_minus_y(std::log(0.5 * (std::sqrt(A) + std::sqrt(A + 4 * std::sqrt(A)))), 1e-2);
  }
  if (std::isinf(x0) || std::isnan(x0))
    printf("ERROR: x0= %f, use_exp2= %d, z=%f, to=%f, tf=%f, sig1=%f, c=%d, det=%f\n", x0, use_exp2, z, to, tf, sig1, c, det);
  auto func = [&](double x) { return fder1(x, z, to, tf, sig1, c); };
  auto fprime = [&](double x) { return fder2(x, z, to, tf, sig1, c); };
  double root;
  try {
    root = newton(func, fprime, x0);
  } catch (const std::runtime_error& err) {
    double a = x0, b = std::isnan(x1) ? x0 : x1;
    double fa = func(a), fb = func(b);
    if (fa * fb > 0) { // should not happen for use_exp2 case, just for safety
      double inc = fa < 0 ? 0.1 : -0.1;
      for (int i = 0; i < 10000; ++i, b+=inc) { // to prevent infinite loop
        fb = func(b);
        if (fa * fb < 0) break;
      }
      if (fa * fb >= 0) throw std::runtime_error("interval not found");
    }
    root = bisect(func, a, b, 100, 1e-2);
  }
  return root;
}

double integ_j(double k, double to, double tf, double sig1, int c, bool return_log,
               double exp2_threshold=3., double h=0.5, int N=200, double ewmax=20.) {
  if (std::isnan(to)) return NAN;
  const double det = std::sqrt(0.5 * x_plus_sqrt_xsq_plus_y(to, 2 * (2 * k + 1)));
  const bool use_exp2 = det < exp2_threshold;
  const double z = use_exp2 ? 2 * k + 2 : 2 * k + 1;
  auto f = use_exp2 ? f1_exp2 : f1_orig2;
  auto fder2 = use_exp2 ? f1_exp2_der2 : f1_orig2_der2;
  const double root = find_root(k, to, tf, sig1, c, det, use_exp2);
  const double f1val = f(root, z, to, tf, sig1, c);
  const double f2der = fder2(root, z, to, tf, sig1, c);
  const double delta = h * std::sqrt(2 / f2der);
  double s = 1; // for i = 0
  for (int sign : {-1, 1}) {
    for (int i = 1; i < N; ++i) {
      const double xx = sign * delta * i + root;
      if (!use_exp2 && xx <= 0) continue; //break?
      const double ff = f(xx, z, to, tf, sig1, c) - f1val;
      s += std::exp(-ff);
      if (ff > ewmax) break;
    }
  }
  const double laplace_correct = s * h;
  const double expon = -f1val + 0.5 * (std::log(2.) - std::log(f2der));
  return return_log ? expon + std::log(laplace_correct) : std::exp(expon) * laplace_correct;
}

double integ_j_ratio(double k_num, double k_den, bool l, double to, double tf, double sig1, int c,
                     double exp2_threshold=3., double h=0.5, int N=200, double ewmax=20.) {
  // factor of sig^{k_num - k_den} is needed, which should be done outside.
  if (std::isnan(to)) return NAN;
  const double det = std::sqrt(0.5 * x_plus_sqrt_xsq_plus_y(to, 2 * (2 * k_den + 1)));
  const bool use_exp2 = det < exp2_threshold;
  const double z = use_exp2 ? 2 * k_den + 2 : 2 * k_den + 1;
  const double deltaz = 2 * (k_num - k_den);
  auto f = use_exp2 ? f1_exp2 : f1_orig2;
  auto fder2 = use_exp2 ? f1_exp2_der2 : f1_orig2_der2;
  const double root = find_root(k_den, to, tf, sig1, c, det, use_exp2);
  const double f1val = f(root, z, to, tf, sig1, c);
  const double f2der = fder2(root, z, to, tf, sig1, c);
  const double delta = h * std::sqrt(2 / f2der);
  auto calc_fom = [&](double xx) { return fom((use_exp2 ? std::exp(xx - std::exp(-xx)) : xx) * tf / sig1, c); };
  const double tmp = use_exp2 ? root - std::exp(-root) : std::log(root);
  double sd = 1, sn = std::exp(deltaz * tmp);
  if (l) sn *= calc_fom(root);
  for (int sign : {-1, 1}) {
    for (int i = 1; i < N; ++i) {
      const double xx = sign * delta * i + root;
      if (!use_exp2 && xx <= 0) continue; //break?
      const double ff = f(xx, z, to, tf, sig1, c) - f1val;
      const double tmp = std::exp(-ff);
      double g = std::exp(deltaz * (use_exp2 ? xx - std::exp(-xx) : std::log(xx)));
      if (l) g *= calc_fom(xx);
      sd += tmp;
      sn += tmp * g;
      if (ff > ewmax) break;
    }
  }
  return sn / sd;
}

// ML intensity target; -log(Io; Fc) without constants
double ll_int(double Io, double sigIo, double k_ani, double S, double Fc, int c) {
  if (std::isnan(Io)) return NAN;
  const double k = c == 1 ? 0 : -0.5;
  const double to = Io / sigIo - sigIo / c / sq(k_ani) / S;
  const double Ic = sq(Fc);
  const double tf = k_ani * Fc / std::sqrt(sigIo);
  const double sig1 = sq(k_ani) * S / sigIo;
  const double logj = integ_j(k, to, tf, sig1, c, true);
  if (c == 1) // acentrics
    return 2 * std::log(k_ani) + std::log(S) + Ic / S - logj;
  else
    return std::log(k_ani) + 0.5 * std::log(S) + 0.5 * Ic / S - logj;
}

// d/dDj -log(Io; Fc)
// note Re(Fcj Fc*) needs to be multiplied
double ll_int_der1_D(double k_ani, double S, double Fc, int c, double eps, double j_ratio_2) {
  const double invepsS = 1. / (S * eps);
  if (c == 1) // acentrics
    return (2 - (3-c) / k_ani / Fc * j_ratio_2) * invepsS;
  else
    return (1. - (3-c) * j_ratio_2 / k_ani / Fc) * invepsS;
}
// d/dS -log(Io; Fc)
double ll_int_der1_S(double k_ani, double S, double Fc, int c, double eps, double j_ratio_1, double j_ratio_2) {
  const double invepsS2 = 1. / (S * S * eps);
  if (c == 1) // acentrics
    return 1. / S - (sq(Fc) + j_ratio_1 / sq(k_ani) / c - (3-c) * Fc * j_ratio_2 / k_ani) * invepsS2;
  else
    return 0.5 / S - 0.5 * sq(Fc) * invepsS2 - (j_ratio_1 / c / k_ani - (3-c) * Fc * j_ratio_2) / k_ani * invepsS2;
}
// k_aniso * d/dk_aniso -log(Io; Fc)
// note k_aniso is multiplied to the derivative
double ll_int_der1_ani(double k_ani, double S, double Fc, int c, double eps, double j_ratio_1, double j_ratio_2) {
  const double invepsS = 1. / (S * eps);
  if (c == 1) // acentrics
    return 2.  - (2 / c / k_ani * j_ratio_1 - (3-c) * Fc * j_ratio_2) / k_ani * invepsS;
  else
    return 1.  - (2 * j_ratio_1 / c / k_ani - (3-c) * Fc * j_ratio_2) * invepsS / k_ani;
}
template<bool for_DS>
py::array_t<double>
ll_int_der1_params_py(py::array_t<double> Io, py::array_t<double> sigIo, py::array_t<double> k_ani,
                      double S, py::array_t<std::complex<double>> Fcs, std::vector<double> Ds,
                      py::array_t<int> c, py::array_t<int> eps) {
  if (Ds.size() != (size_t)Fcs.shape(1)) throw std::runtime_error("Fc and D shape mismatch");
  const size_t n_models = Fcs.shape(1);
  const size_t n_ref = Fcs.shape(0);
  const size_t n_cols = for_DS ? n_models + 1 : 1;
  auto Io_ = Io.unchecked<1>();
  auto sigIo_ = sigIo.unchecked<1>();
  auto k_ani_ = k_ani.unchecked<1>();
  auto Fcs_ = Fcs.unchecked<2>();
  auto c_ = c.unchecked<1>();
  auto eps_ = eps.unchecked<1>();

  // der1 wrt D1, D2, .., S, or k_ani
  auto ret = py::array_t<double>({n_ref, n_cols});
  double* ptr = (double*) ret.request().ptr;
  auto sum_Fc = [&](int i) {
                  std::complex<double> s = Fcs_(i, 0) * Ds[0];
                  for (size_t j = 1; j < n_models; ++j)
                    s += Fcs_(i, j) * Ds[j];
                  return s;
                };
  for (size_t i = 0; i < n_ref; ++i) {
    if (std::isnan(Io_(i))) {
      for (size_t j = 0; j < n_cols; ++j)
        ptr[i * n_cols + j] = NAN;
      continue;
    }
    const std::complex<double> Fc_total_conj = std::conj(sum_Fc(i));
    const double Fc_abs = std::abs(Fc_total_conj);
    const double to = Io_(i) / sigIo_(i) - sigIo_(i) / c_(i) / sq(k_ani_(i)) / S / eps_(i);
    const double sqrt_sigIo = std::sqrt(sigIo_(i));
    const double tf = k_ani_(i) * Fc_abs / sqrt_sigIo;
    const double sig1 = sq(k_ani_(i)) * S * eps_(i) / sigIo_(i);
    const double k_num_1 = c_(i) == 1 ? 1. : 0.5;
    const double k_num_2 = c_(i) == 1 ? 0.5 : 0.;
    const double j_ratio_1 = integ_j_ratio(k_num_1, k_num_1 - 1, false, to, tf, sig1, c_(i)) * sigIo_(i);
    const double j_ratio_2 = integ_j_ratio(k_num_2, k_num_2 - 0.5, true, to, tf, sig1, c_(i)) * sqrt_sigIo;
    if (for_DS) {
      const double tmp = ll_int_der1_D(k_ani_(i), S, Fc_abs, c_(i), eps_(i), j_ratio_2);
      for (size_t j = 0; j < n_models; ++j) {
        const double r_fcj_fc = (Fcs_(i, j) * Fc_total_conj).real();
        ptr[i*n_cols + j] = tmp * r_fcj_fc;
      }
      ptr[i*n_cols + n_models] = ll_int_der1_S(k_ani_(i), S, Fc_abs, c_(i), eps_(i), j_ratio_1, j_ratio_2);
    }
    else
      ptr[i] = ll_int_der1_ani(k_ani_(i), S, Fc_abs, c_(i), eps_(i), j_ratio_1, j_ratio_2);
  }
  return ret;
}

// For French-Wilson
template<bool for_S>
py::array_t<double>
ll_int_fw_der1_params_py(py::array_t<double> Io, py::array_t<double> sigIo, py::array_t<double> k_ani,
                         double S, py::array_t<int> c, py::array_t<int> eps) {
  size_t n_ref = Io.shape(0);
  auto Io_ = Io.unchecked<1>();
  auto sigIo_ = sigIo.unchecked<1>();
  auto k_ani_ = k_ani.unchecked<1>();
  auto c_ = c.unchecked<1>();
  auto eps_ = eps.unchecked<1>();

  // der1 wrt S or k_ani
  auto ret = py::array_t<double>(n_ref);
  double* ptr = (double*) ret.request().ptr;
  for (size_t i = 0; i < n_ref; ++i) {
    if (std::isnan(Io_(i))) {
      ptr[i] = NAN;
      continue;
    }
    const double to = Io_(i) / sigIo_(i) - sigIo_(i) / c_(i) / sq(k_ani_(i)) / S / eps_(i);
    const double k_num = c_(i) == 1 ? 1. : 0.5;
    const double j_ratio_1 = integ_j_ratio(k_num, k_num - 1, false, to, 0., 0., c_(i)) * sigIo_(i);
    if (for_S)
      ptr[i] = ll_int_der1_S(k_ani_(i), S, 0., c_(i), eps_(i), j_ratio_1, 0.);
    else
      ptr[i] = ll_int_der1_ani(k_ani_(i), S, 0., c_(i), eps_(i), j_ratio_1, 0.);
  }
  return ret;
}

void add_intensity(py::module& m) {
  m.def("integ_J", py::vectorize(integ_j),
        py::arg("k"), py::arg("to"), py::arg("tf"), py::arg("sig1"), py::arg("c"), py::arg("return_log"),
        py::arg("exp2_threshold")=10, py::arg("h")=0.5, py::arg("N")=200, py::arg("ewmax")=20.);
  m.def("integ_J_ratio", py::vectorize(integ_j_ratio),
        py::arg("k_num"), py::arg("k_den"), py::arg("l"), py::arg("to"), py::arg("tf"),
        py::arg("sig1"), py::arg("c"),
        py::arg("exp2_threshold")=10, py::arg("h")=0.5, py::arg("N")=200, py::arg("ewmax")=20.);
  m.def("ll_int", py::vectorize(ll_int),
        py::arg("Io"), py::arg("sigIo"), py::arg("k_ani"), py::arg("S"), py::arg("Fc"), py::arg("c"));
  m.def("ll_int_der1_DS", &ll_int_der1_params_py<true>);
  m.def("ll_int_der1_ani", &ll_int_der1_params_py<false>);
  m.def("ll_int_fw_der1_S", &ll_int_fw_der1_params_py<true>);
  m.def("ll_int_fw_der1_ani", &ll_int_fw_der1_params_py<false>);
  m.def("lambertw", py::vectorize(lambertw::lambertw));
}
