/* This is BIGsplines.h, a header file of the
   NumericPython BIGsplines toolbox

   Jan Kybic, August 2000

   $Id: BIGsplines.h,v 1.1 2005/10/07 15:45:06 eav Exp $
*/

#include <stdlib.h>
#include <stdio.h>
#include <Python.h>
#include <arrayobject.h>

#define ERROR (1)
#define OK    (0)

/* to be used in Philippe's toolbox routines */
#define WRITE_ERROR(x,s) BSerrormsg(s) ;
#define DEBUG_CHECK_NULL_POINTER(a,b,c,d) 
#define DEBUG_CHECK_RANGE_LONG(a,b,c,d,e,f)
#define DEBUG_RETURN_ON_ERROR(a,b)
#define DEBUG_WRITE_ENTERING(a,b)
#define DEBUG_WRITE_LEAVING(a,b)

/* to be used by my splninterp.c */

#define myErrMsg(s) BSerrormsg(s) 
#define myMalloc(ptr,a,b) \
 if ((ptr=(void *)malloc((a)*(b)*sizeof(double)))==NULL) \
   { myErrMsg("could not malloc") ; return ERROR ; }
#define myMallocInt(ptr,a,b) \
 if ((ptr=(void *)malloc((a)*(b)*sizeof(int)))==NULL) \
   { myErrMsg("could not malloc") ; return ERROR ; }
#define myFree(x) free(x)
#define mexPrintf printf

void BSerrormsg(char *s) ; /* prints an error message */

/* -------------- Enum and prototype for fiir.c ---------- */

enum TBoundaryConvention
{ /* WARNING: needs to be consistent with bigsplines.py */
  AntiMirrorOnBounds=0,
  FiniteCoefficientSupport=1,
  FiniteDataSupport=2,
  MirrorOffBounds=3,
  MirrorOnBounds=4,
  Periodic=5
};

int		IirConvolvePoles
(
 double	InputData[],		/* data to process */
 double	OutputData[],		/* result */
 long	SignalLength,		/* length of the 1D data array */
 double	RealPoles[],		/* array of real poles */
 long	PoleNumber,		/* number of poles */
 enum TBoundaryConvention
 Convention,			/* boundary convention */
 double	Tolerance		/* admissible relative error */
 );

/* -------------- Prototypes for ffir.c ---------- */

extern int              FirConvolve
(
 double  InputData[],            /* data to process */
 double  OutputData[],           /* result */
 long    SignalLength,           /* length of the 1D data array */
 double  Kernel[],
 /* kernel */
 long    KernelOrigin,           /* center of the kernel */
 long    KernelLength,           /* length of the 1D kernel */
 enum TBoundaryConvention Convention  /* boundary convention */
 ) ;

extern int convolve_subsamp(double *x, int xn, double *y, int yn, 
			    double *k, int kn, int ofs, int shift) ;
/* convolves a signal x of length x with a kernel k of length k.
   first scalar product is computed at offset ofs, 
   i.e. sum(x[ofs..ofs+kn-1]*k[0..kn-1]), the next one at
   ofs+shift, etc., yn of them in total. The signal x is assumed to be
   zero outside the boundaries. */

extern int convolve_upsample(double *x, int xn, double *y, 
			     double *k, int kn, int ko, int step) ;
/* Convolves an upsampled version of x with a kernel k of length kn, */
/* with a center point ko. The result is stored into y of size
   (xn-1)*step+1. MirrorOnBounds conditions are assumed */

/* -------------- Prototypes for bsplneval.c ---------- */

double bspln3(double x) ;
double bspln2(double x) ;
double bspln2d(double x) ;
double bspln2dd(double x) ;
double bspln1(double x) ;
double bspln0(double x) ;
double bspln1d(double x) ;
double bspln3d(double x) ;
double bspln3dd(double x) ;
int choosespln(int degree,double (**fp)(double),int *sp,int type) ;


/* -------------- Prototypes for splninterp.c ---------- */

int evalbspln(double *x,double *y, int n, int degree) ;
/* evaluates a B-spline at n points given by the vector x */

int    splinterp (
 PyArrayObject *coefsarray,                 /* B-spline coefficients */
 PyArrayObject *coordsarray,		        /* 3D coordinates */
 PyArrayObject *outputarray,                /* output values, one for each coord */
 int	degree,                 /* 0 - Haar, 1 - Linear etc. */
 int    dflag,                  /* 0 - value, 1,4,16 - first derivative with 
                                   respect to x,y,z ; 2,8,32 - second der. */
 int    bcond                   /* boundary condation */
 ) ;

double mfolddmirroroffbound(double k,int n) ;
int mfoldmirroroffbound(int k,int n) ;
int mfoldmirroronbound(int k,int n) ;
double mfolddmirroronbound(double k,int n) ;

/* -------------- Prototypes for bigsdcgr.c --------------  */

int bigsdcgr(double *fr,  /* reference image */
	      double *E,   /* the criterion value */
	      double *gr,  /* the gradient */
	      int degc,  /* degree for the coefficients */
	      int frx, int fry, /* size of the reference image */
	      int cx, int cy,    /* size of the image coefficients */
	      double *derw, /* first derivatives */
	      double *fw   /* warped test image */
	      ) ;

/* -------------------------------------------------------- */

#define max(a,b) ((a)>(b) ? (a) : (b))
#define min(a,b) ((a)>(b) ? (b) : (a))

/* -------------- end of BIGsplines.h --------------------- */
