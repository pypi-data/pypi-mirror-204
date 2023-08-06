#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <math.h>

/**
 * Compute the resulting strain energy density for edge dislocations.
 *
 * @param m_x Measurement point x-coordinate.
 * @param m_y Measurement point y-coordinate.
 * @param d_x Dislocation x-coordinates.
 * @param d_y Dislocation y-coordinates.
 * @param senses Dislocation Burgers vector senses.
 * @param number Number of dislocations.
 * @param core_2 Squared core radius.
 * @param poisson Poisson number.
 * @param keep Consider the point.
 * @param energy Strain energy density.
 */
void edge(
    double m_x,
    double m_y,
    double* d_x,
    double* d_y,
    signed char* senses,
    size_t number,
    double core_2,
    double poisson,
    int* keep,
    double* energy
)
{
    double r_x;
    double r_y;
    double x_2;
    double y_2;
    double r_2;
    double r_4;
    double strain_xx = 0;
    double strain_yy = 0;
    double stress_xx = 0;
    double stress_yy = 0;
    double xy = 0;
    double c_1 = 2 * (1 - poisson);
    double c_2;
    double c_3;
    double c_4;
    for(size_t i=0; i<number; i++)
    {
        r_x = d_x[i] - m_x;
        r_y = d_y[i] - m_y;
        x_2 = r_x * r_x;
        y_2 = r_y * r_y;
        r_2 = x_2 + y_2;
        if (r_2 < core_2)
        {
            *keep = 0;
            return;
        }
        r_4 = r_2 * r_2;
        c_2 = x_2 - y_2;
        c_3 = 3 * x_2 + y_2;
        c_4 = r_y / r_2;
        strain_xx -= senses[i] * c_4 * (c_2 / r_2 + c_1);
        strain_yy += senses[i] * c_4 * (c_3 / r_2 - c_1);
        stress_xx -= senses[i] * r_y * c_3 / r_4;
        stress_yy += senses[i] * r_y * c_2 / r_4;
        xy += senses[i] * r_x * c_2 / r_4;
    }
    *energy += strain_xx*stress_xx + strain_yy*stress_yy + 2*xy*xy;
}

/**
 * Compute the resulting strain energy density for screw dislocations.
 *
 * @param m_x Measurement point x-coordinate.
 * @param m_y Measurement point y-coordinate.
 * @param d_x Dislocation x-coordinates.
 * @param d_y Dislocation y-coordinates.
 * @param senses Dislocation Burgers vector senses.
 * @param number Number of dislocations.
 * @param core_2 Squared core radius.
 * @param keep Consider the point.
 * @param energy Strain energy density.
 */
void screw(
    double m_x,
    double m_y,
    double* d_x,
    double* d_y,
    signed char* senses,
    size_t number,
    double core_2,
    int* keep,
    double* energy
)
{
    double r_x;
    double r_y;
    double r_2;
    double xz = 0;
    double yz = 0;
    for(size_t i=0; i<number; i++)
    {
        r_x = d_x[i] - m_x;
        r_y = d_y[i] - m_y;
        r_2 = r_x*r_x + r_y*r_y;
        if (r_2 < core_2)
        {
            *keep = 0;
            return;
        }
        xz += senses[i] * r_y / r_2;
        yz += senses[i] * r_x / r_2;
    }
    *energy = 2 * (xz*xz + yz*yz);
}

/**
 * Python edge wrapper function.
 *
 * @param PyObject
 * @param args
 * @return the strain energy density.
 */
static PyObject *py_edge(
    PyObject *self,
    PyObject *args
)
{
    double m_x;
    double m_y;
    PyObject *obj_d_x;
    Py_buffer buf_d_x;
    PyObject *obj_d_y;
    Py_buffer buf_d_y;
    PyObject *obj_senses;
    Py_buffer buf_senses;
    double core;
    double poisson;
    double energy = 0;
    int keep = 1;
    if (!PyArg_ParseTuple(args, "ddOOOdd", &m_x, &m_y, &obj_d_x, &obj_d_y, &obj_senses, &core, &poisson))
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_d_x, &buf_d_x, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_d_y, &buf_d_y, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_senses, &buf_senses, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    edge(m_x, m_y, buf_d_x.buf, buf_d_y.buf, buf_senses.buf, buf_senses.shape[0], core*core, poisson, &keep, &energy);
    return Py_BuildValue("di", energy, keep);
}

/**
 * Python screw wrapper function.
 *
 * @param PyObject
 * @param args
 * @return the strain energy density.
 */
static PyObject *py_screw(
    PyObject *self,
    PyObject *args
)
{
    double m_x;
    double m_y;
    PyObject *obj_d_x;
    Py_buffer buf_d_x;
    PyObject *obj_d_y;
    Py_buffer buf_d_y;
    PyObject *obj_senses;
    Py_buffer buf_senses;
    double core;
    double energy = 0;
    int keep = 1;
    if (!PyArg_ParseTuple(args, "ddOOOd", &m_x, &m_y, &obj_d_x, &obj_d_y, &obj_senses, &core))
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_d_x, &buf_d_x, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_d_y, &buf_d_y, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_senses, &buf_senses, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    screw(m_x, m_y, buf_d_x.buf, buf_d_y.buf, buf_senses.buf, buf_senses.shape[0], core*core, &keep, &energy);
    return Py_BuildValue("di", energy, keep);
}

static PyMethodDef EnergyModule[] = {
    {
        "edge",
        py_edge,
        METH_VARARGS,
        "Compute the resulting strain energy density for edge dislocations."
    },
    {
        "screw",
        py_screw,
        METH_VARARGS,
        "Compute the resulting strain energy density for screw dislocations."
    },
    {
        NULL,
        NULL,
        0,
        NULL
    }
};

static struct PyModuleDef energymodule = {
    PyModuleDef_HEAD_INIT,
    "energy", // module name
    NULL,  // module documentation
    -1,
    EnergyModule
};

PyMODINIT_FUNC PyInit_energy(void)
{
    return PyModule_Create(&energymodule);
}
