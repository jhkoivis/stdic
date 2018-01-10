/* This is BIGsplines.c, the main C code file for the

   NumericPython BIGsplines toolbox

   Jan Kybic, August 2000

   $Id: BIGsplines.c,v 1.1 2005/10/07 15:45:06 eav Exp $

   Port from Numeric to numpy by Simo Tuomisto, 2010

*/

#include "Python.h"
#include "BIGsplines.h"
#include "arrayobject.h"

static PyObject *ErrorObject ; /* Exception object (string) */

/* sets error message for an exception to pass to Python */
/* it is used by WRITE_ERROR used in fiir.c */
void BSerrormsg(char *s) { PyErr_SetString(ErrorObject, s) ; }


/* ------ here the glue functions start ------ */

/* IIR filtering */
/* Python usage: y=IirConvolvePoles(input,poles,bcond) */

static PyObject *BSiirConvolvePoles(PyObject *self, PyObject *args)
{
  PyObject *input,*poles ;
  PyArrayObject *inputarray,*polesarray,*outputarray ;
  int bcond ;

  /* parse input */
  if (!PyArg_ParseTuple(args,"OOi",&input,&poles,&bcond)) return NULL ;

  /* convert to arrays (actually, only vectors are accepted) */
  if ((inputarray=(PyArrayObject *)PyArray_ContiguousFromAny(input,
       PyArray_DOUBLE,1,1))==NULL) return NULL ;
  if ((polesarray=(PyArrayObject *)PyArray_ContiguousFromAny(poles,
       PyArray_DOUBLE,1,1))==NULL) {
    Py_DECREF(inputarray) ; return NULL ; }

  /* create output array */
  if ((outputarray=(PyArrayObject *)PyArray_SimpleNew(1,
       PyArray_DIMS(inputarray),PyArray_DOUBLE))==NULL) {
    Py_DECREF(inputarray) ; Py_DECREF(polesarray) ; return NULL ; }

  /* do the real work */  
  if (IirConvolvePoles((double *)inputarray->data,(double *)outputarray->data,
                   (long int)PyArray_DIM(inputarray,0),(double *)polesarray->data,
		            (long int)PyArray_DIM(polesarray, 0),bcond,1e-20)==ERROR) {
    Py_DECREF(inputarray) ; Py_DECREF(polesarray) ; Py_DECREF(outputarray) ;
    return NULL ; 
  }

  /* decrement reference counters */
  Py_DECREF(inputarray) ;
  Py_DECREF(polesarray) ;
  /* and return */
  return PyArray_Return(outputarray) ;
}

/* FIR filtering */
/* Python usage: y=FirConvolve(input,kernel,kernelorigin,bcond) */

static PyObject *BSfirConvolve(PyObject *self, PyObject *args)
{
  PyObject *input,*kernel ;
  PyArrayObject *inputarray,*kernelarray,*outputarray ;
  int kernelorigin,bcond ;

  /* parse input */
  if (!PyArg_ParseTuple(args,"OOii",&input,&kernel,
			&kernelorigin,&bcond)) return NULL ;

  /* convert to arrays (actually, only vectors are accepted) */
  if ((inputarray=(PyArrayObject *)PyArray_ContiguousFromAny(input,
       PyArray_DOUBLE,1,1))==NULL) return NULL ;
  if ((kernelarray=(PyArrayObject *)PyArray_ContiguousFromAny(kernel,
       PyArray_DOUBLE,1,1))==NULL) {
    Py_DECREF(inputarray) ; return NULL ; }

  /* create output array */
  if ((outputarray=(PyArrayObject *)PyArray_SimpleNew(1,
       PyArray_DIMS(inputarray),PyArray_DOUBLE))==NULL) {
    Py_DECREF(inputarray) ; Py_DECREF(kernelarray) ; return NULL ; }

  /* do the real work */  
  FirConvolve((double *)inputarray->data,(double *)outputarray->data,
                   (long)PyArray_DIM(inputarray,0),(double *)kernelarray->data,
		   kernelorigin,PyArray_DIM(kernelarray,0),bcond) ;

  /* decrement reference counters */
  Py_DECREF(inputarray) ;
  Py_DECREF(kernelarray) ;
  /* and return */
  return PyArray_Return(outputarray) ;
}

/* ----------------------------------------------------------------- */
/* Spline interpolation */
/* Python usage: y=SplineInterpol(coefs,coords,degree,flag,bcond)    */
/*                                                                   */
/* R^n->R^1 function is interpolated by spline of degree degree      */
/* with Bspline coeficients coefs. It is evaluated at points coords  */
/* coefs is always n-dimensional, coords n+1 dimensional, the last   */
/* (fastest changing) dimension contains the coordinates             */
/* where degree 0=constant, 1=linear ...                             */
/*       dflag 1,4,16 - first derivative with respect to x,y,z       */ 
/*             2,8,32 - second der. combinations possible            */

#define BSSIMAXDIM (3) /* maximum number of dimensions */

static PyObject *BSsplineInterpol(PyObject *self, PyObject *args)
{
  PyArrayObject *coefs,*coords;
  PyArrayObject *coefsarray,*coordsarray,*outputarray ;
  int degree,flag ;
  int ncoord,ncoef,bcond ;

  /* parse input */
  if (!PyArg_ParseTuple(args,"OOiii",&coefs,&coords,
			&degree,&flag,&bcond)) return NULL ;

  /* convert to arrays (actually, only vectors are accepted) */
  
  if ((coefsarray=PyArray_GETCONTIGUOUS(coefs))==NULL) return NULL;
  if ((coordsarray=PyArray_GETCONTIGUOUS(coords))==NULL) { Py_DECREF(coefsarray); return NULL; }
  
  /* The first dimension of coords must be equal to the number of dimensions
     in coefs */
  ncoord=coordsarray->nd ; ncoef=coefsarray->nd ;
  if (PyArray_DIM(coordsarray,ncoord-1)!=ncoef) {
    BSerrormsg("last dim of coords must be equal to the no of dim of coefs") ;
  err2:
    Py_DECREF(coefsarray) ; Py_DECREF(coordsarray) ; return NULL ; }
  if (PyArray_DIM(coordsarray,ncoord-1)>BSSIMAXDIM) {
    BSerrormsg("last dim of coords is too big") ;
    goto err2 ; }

  /* create output array */
  /*
  if ((outputarray=(PyArrayObject *)PyArray_SimpleNew(coordsarray->nd-1,
       PyArray_DIMS(coordsarray),PyArray_DOUBLE))==NULL) goto err2 ; 
  */
  if ((outputarray=(PyArrayObject *)PyArray_SimpleNew(coordsarray->nd-1,
       PyArray_DIMS(coordsarray),PyArray_DOUBLE))==NULL) goto err2 ;
       
  /* do the real work */  
  if (splinterp(coefsarray,coordsarray,outputarray,degree,flag,bcond)==ERROR) 
  {
    Py_DECREF(coefsarray) ; Py_DECREF(coordsarray) ; Py_DECREF(outputarray) ;
    return NULL ; 
  }
  /* decrement reference counters */
  Py_DECREF(coefsarray) ;
  Py_DECREF(coordsarray) ;
  /* and return */
  return PyArray_Return(outputarray) ;
}

/* ----------------------------------------------------------------- */
/* Evaluates B-spline of degree 'degree' at n-points x[0],...,x[n-1] */
/* Python usage: y=BSevalbspln(x,degree)                             */

static PyObject *BSevalbspln(PyObject *self, PyObject *args)
{
  PyObject *x ;
  PyArrayObject *xarr,*yarr ;
  int degree ;

  if (!PyArg_ParseTuple(args,"Oi",&x,&degree)) 
    return NULL ;
  if ((xarr=(PyArrayObject *)PyArray_ContiguousFromAny(x,
       PyArray_DOUBLE,1,1))==NULL) return NULL ;
  if ((yarr=(PyArrayObject *)PyArray_SimpleNew(xarr->nd,PyArray_DIMS(xarr),
					     PyArray_DOUBLE))==NULL)
    { err3:
         Py_DECREF(xarr) ; return NULL ; }
  if (evalbspln((double *)xarr->data,(double *)yarr->data,
		xarr->dimensions[0],degree))
    { Py_DECREF(yarr) ; goto err3 ; }

  Py_DECREF(xarr) ;
  return PyArray_Return(yarr) ;
}

/* ConvolveSubsamp performs an equivalent of a convolution */
/* (with reversed kernel!) followed by downsampling. Signal is */
/* assumed to be zero outside the boundaries */
/* Python usage: y=ConvolveSubsamp(x,kernel,yn,ofs,shift) */
/* where ofs is the starting ofset in x, shift is added to the position */
/* for each output point, and yn is the total number of output points */
/* Only works for 1D arrays. */

static PyObject *BSconvolveSubsamp(PyObject *self, PyObject *args)
{
  PyObject *x,*kernel ;
  PyArrayObject *xarr,*yarr,*kernelarr ;
  npy_intp yn;
  int ofs,shift ;

  if (!PyArg_ParseTuple(args,"OOiii",&x,&kernel,&yn,&ofs,&shift)) 
    return NULL ;
  if ((xarr=(PyArrayObject *)PyArray_ContiguousFromAny(x,
       PyArray_DOUBLE,1,1))==NULL) return NULL ;
  if ((kernelarr=(PyArrayObject *)PyArray_ContiguousFromAny(kernel,
       PyArray_DOUBLE,1,1))==NULL) 
    { Py_DECREF(xarr) ; return NULL ;}
  if ((yarr=(PyArrayObject *)PyArray_SimpleNew(1,&yn,
					     PyArray_DOUBLE))==NULL)
    { Py_DECREF(xarr) ; Py_DECREF(kernelarr) ; return NULL ;}

  if (convolve_subsamp((double *)xarr->data,xarr->dimensions[0],
		      (double *)yarr->data,(int)yn,
		      (double *)kernelarr->data,
		       kernelarr->dimensions[0],ofs,shift))
    { Py_DECREF(xarr) ; Py_DECREF(kernelarr) ;
      Py_DECREF(yarr) ; return NULL ;}
  Py_DECREF(xarr) ; Py_DECREF(kernelarr) ;
  return PyArray_Return(yarr) ;
}

/* ConvolveUpsample performs an equivalent of upsampling followed */
/* by convolution (with reversed kernel). The signal is assumed to be zero */
/* outside the boundaries */
/* Python usage: y=ConvolveUpsample(x,kernel,korig,step) */
/* where korig is the center of the kernel and step is the upsampling */
/* factor. Only works for 1D arrays. */

static PyObject *BSconvolveUpsample(PyObject *self, PyObject *args)
{
  PyObject *x,*kernel ;
  PyArrayObject *xarr,*yarr,*kernelarr ;
  int korig,step;
  npy_intp yn ;

  if (!PyArg_ParseTuple(args,"OOii",&x,&kernel,&korig,&step)) 
    return NULL ;
  if ((xarr=(PyArrayObject *)PyArray_ContiguousFromAny(x,
       PyArray_DOUBLE,1,1))==NULL) return NULL ;
  if ((kernelarr=(PyArrayObject *)PyArray_ContiguousFromAny(kernel,
       PyArray_DOUBLE,1,1))==NULL) 
    { Py_DECREF(xarr) ; return NULL ;}
  yn=(xarr->dimensions[0]-1)*step+1 ;
  if ((yarr=(PyArrayObject *)PyArray_SimpleNew(1,&yn,
       PyArray_DOUBLE))==NULL)
    { Py_DECREF(xarr) ; Py_DECREF(kernelarr) ; return NULL ;}

  if (convolve_upsample((double *)xarr->data,xarr->dimensions[0],
		      (double *)yarr->data,
		      (double *)kernelarr->data,
		       kernelarr->dimensions[0],korig,step))
    { Py_DECREF(xarr) ; Py_DECREF(kernelarr) ;
      Py_DECREF(yarr) ; return NULL ;}
  Py_DECREF(xarr) ; Py_DECREF(kernelarr) ;
  return PyArray_Return(yarr) ;
}



/* ---------- table of functions in our module --------------- */

static struct PyMethodDef BIGsplines_methods[]={
  { "IirConvolvePoles",  BSiirConvolvePoles, METH_VARARGS },
  { "SplineInterpol", BSsplineInterpol, METH_VARARGS },
  { "FirConvolve", BSfirConvolve, METH_VARARGS },
  { "Evalbspln", BSevalbspln, METH_VARARGS },
  { "ConvolveSubsamp", BSconvolveSubsamp, METH_VARARGS },
  { "ConvolveUpsample", BSconvolveUpsample, METH_VARARGS },
  { NULL, NULL} /* stop mark */
} ;

/* ----------- module initialization -------------------------- */
void initBIGsplines() {
  PyObject *m,*d ;

  m=Py_InitModule("BIGsplines",BIGsplines_methods) ; /* register methods */

  /* initialize exception object */
  d=PyModule_GetDict(m) ; /* get module dictionary */
  ErrorObject=PyErr_NewException("BIGsplines.error",NULL,NULL) ;
  PyDict_SetItemString(d,"error",ErrorObject) ;

  import_array() ;

  if (PyErr_Occurred()) /* something went wrong ?*/
    Py_FatalError("can't initialize module BIGsplines") ;
}


/* ---------- end of BIGsplines.c ---------- */
