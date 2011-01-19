/* This is ffir.c, a FIR filtering routine by Philippe Thevenaz
   Modified by Jan Kybic, August 2000

   part of NumericPython BIGsplines toolbox
   $Id: ffir.c,v 1.1 2005/10/07 15:45:06 eav Exp $

   Usage:

	FirConvolve(x,y,nx,kernel,kernelorigin,kernellength) ;

   where x is the input, y output
   
*/

#include <math.h>
#include <unistd.h> /* for ptrdiff_t */

#ifndef DARWIN /* osx uses different malloc.h */
#include <malloc.h> /* for ptrdiff_t */
#else
#include <sys/malloc.h>
#include <stddef.h> /* for ptrdiff_t */
#endif

#include "BIGsplines.h"


/*--------------------------------------------------------------------------*/

int		FirConvolve
(
 double	InputData[],		/* data to process */
 double	OutputData[],		/* result */
 long	SignalLength,		/* length of the 1D data array */
 double	Kernel[],			/* kernel */
 long	KernelOrigin,		/* center of the kernel */
 long	KernelLength,		/* length of the 1D kernel */
 enum TBoundaryConvention
 Convention			/* boundary convention */
 )

     /* the specified boundary convention applies to the input data only, not to the kernel */
     /* the boundary convention applied to the kernel is FiniteDataSupport */
     /* the input and the output have the same length */
     /* the origin for the kernel is given with respect to the leftmost sample [0] */
     /* success: return(!ERROR); failure: return(ERROR) */
     /* general structure is as follows:
	for (i = 0L; (i < SignalLength); i++) {
	Sum = 0.0;
	for (j = -Infinity; (j <= Infinity); j++) {
	Sum += InputData[j] * Kernel[KernelOrigin + i - j];
	}
	OutputData[i] = Sum;
	}
     */

{ /* begin FirConvolve */

  double	*p, *q;
  double	f0, fk, fn, df;
  double	Sum;
  long	i, j, k;
  long	m, n;
  long	n2;
  long	kp, km;
  int		Status = !ERROR;

  /**/DEBUG_CHECK_NULL_POINTER(FirConvolve, InputData, Status,
			       /**/	"No input data")
	/**/DEBUG_CHECK_NULL_POINTER(FirConvolve, OutputData, Status,
				     /**/	"No output data")
	/**/DEBUG_CHECK_RANGE_LONG(FirConvolve, SignalLength, 1L, LONG_MAX, Status,
				   /**/	"Invalid signal length (should be strictly positive)")
	/**/DEBUG_CHECK_NULL_POINTER(FirConvolve, Kernel, Status,
				     /**/	"No kernel")
	/**/DEBUG_CHECK_RANGE_LONG(FirConvolve, KernelLength, 1L, LONG_MAX, Status,
				   /**/	"Invalid kernel length (should be strictly positive)")
	/**/DEBUG_RETURN_ON_ERROR(FirConvolve, Status)
	/**/DEBUG_WRITE_ENTERING(FirConvolve,
				 /**/	"About to perform FIR convolution")

	switch (Convention) {
	case AntiMirrorOnBounds:
	  /* More optimization needed for better efficiency in AntiMirrorOnBounds */
	  Kernel += (ptrdiff_t)(KernelLength - 1L);
	  if (SignalLength == 1L) {
	    Sum = 0.0;
	    for (j = -KernelLength; (j < 0L); j++) {
	      Sum += *Kernel--;
	    }
	    *OutputData = *InputData * Sum;
	  }
	  else {
	    n2 = 2L * (SignalLength - 1L);
	    f0 = *InputData;
	    fn = InputData[SignalLength - 1L];
	    df = fn - f0;
	    m = 1L + KernelOrigin - KernelLength;
	    km = m;
	    m -= (m < 0L) ? (n2 * ((m + 1L - n2) / n2)) : (n2 * (m / n2));
	    for (i = 0L; (i < SignalLength); km++, i++) {
	      q = Kernel;
	      k = m;
	      kp = km;
	      Sum = 0.0;
	      for (j = -KernelLength; (j < 0L); kp++, j++) {
		fk = (k < SignalLength) ? (InputData[k]) : (2.0 * fn - InputData[n2 - k]);
		Sum += ((double)((kp - k) / (SignalLength - 1L)) * df + fk) * *q--;
		if (++k == n2) {
		  k = 0L;
		}
	      }
	      if (++m == n2) {
		m = 0L;
	      }
	      *OutputData++ = Sum;
	    }
	  }
	  break;
	case FiniteDataSupport:
	  Kernel += (ptrdiff_t)(KernelLength - 1L);
	  k = KernelOrigin - (KernelLength - 1L);
	  for (i = -SignalLength; (i < 0L); k++, i++) {
	    kp = (0L < k) ? (k) : (0L);
	    km = k - kp;
	    p = InputData + (ptrdiff_t)kp;
	    q = Kernel + (ptrdiff_t)km;
	    Sum = 0.0;
	    for (j = kp - ((SignalLength < (k + KernelLength)) ? (SignalLength)
			   : (k + KernelLength)); (j < 0L); j++) {
	      Sum += *p++ * *q--;
	    }
	    *OutputData++ = Sum;
	  }
	  break;
	case MirrorOffBounds:
	  Kernel += (ptrdiff_t)(KernelLength - 1L);
	  if (SignalLength == 1L) {
	    Sum = 0.0;
	    for (j = -KernelLength; (j < 0L); j++) {
	      Sum += *Kernel--;
	    }
	    *OutputData = *InputData * Sum;
	  }
	  else {
	    n2 = 2L * SignalLength;
	    m = 1L + KernelOrigin - KernelLength;
	    m -= (m < 0L) ? (n2 * ((m + 1L - n2) / n2)) : (n2 * (m / n2));
	    for (i = 0L; (i < SignalLength); i++) {
	      j = -KernelLength;
	      k = m;
	      q = Kernel;
	      Sum = 0.0;
	      while (j < 0L) {
		p = InputData + (ptrdiff_t)k;
		kp = ((k - SignalLength) < j) ? (j) : (k - SignalLength);
		if (kp < 0L) {
		  for (n = kp; (n < 0L); n++) {
		    Sum += *p++ * *q--;
		  }
		  k -= kp;
		  j -= kp;
		}
		p = InputData + (ptrdiff_t)(n2 - k - 1L);
		km = ((k - n2) < j) ? (j) : (k - n2);
		if (km < 0L) {
		  for (n = km; (n < 0L); n++) {
		    Sum += *p-- * *q--;
		  }
		  j -= km;
		}
		k = 0L;
	      }
	      if (++m == n2) {
		m = 0L;
	      }
	      *OutputData++ = Sum;
	    }
	  }
	  break;
	case MirrorOnBounds:
	  Kernel += (ptrdiff_t)(KernelLength - 1L);
	  if (SignalLength == 1L) {
	    Sum = 0.0;
	    for (j = -KernelLength; (j < 0L); j++) {
	      Sum += *Kernel--;
	    }
	    *OutputData = *InputData * Sum;
	  }
	  else {
	    n2 = 2L * (SignalLength - 1L);
	    m = 1L + KernelOrigin - KernelLength;
	    m -= (m < 0L) ? (n2 * ((m + 1L - n2) / n2)) : (n2 * (m / n2));
	    for (i = 0L; (i < SignalLength); i++) {
	      j = -KernelLength;
	      k = m;
	      q = Kernel;
	      Sum = 0.0;
	      while (j < 0L) {
		p = InputData + (ptrdiff_t)k;
		kp = ((k - SignalLength) < j) ? (j) : (k - SignalLength);
		if (kp < 0L) {
		  for (n = kp; (n < 0L); n++) {
		    Sum += *p++ * *q--;
		  }
		  k -= kp;
		  j -= kp;
		}
		p = InputData + (ptrdiff_t)(n2 - k);
		km = ((k - n2) < j) ? (j) : (k - n2);
		if (km < 0L) {
		  for (n = km; (n < 0L); n++) {
		    Sum += *p-- * *q--;
		  }
		  j -= km;
		}
		k = 0L;
	      }
	      if (++m == n2) {
		m = 0L;
	      }
	      *OutputData++ = Sum;
	    }
	  }
	  break;
	case Periodic:
	  Kernel += (ptrdiff_t)(KernelLength - 1L);
	  k = KernelOrigin - (KernelLength - 1L);
	  k = (k < 0L) ? (k + SignalLength * ((SignalLength - 1L - k) / SignalLength))
	    : ((SignalLength <= k) ? (k - SignalLength * (k / SignalLength)) : (k));
	  for (i = -SignalLength; (i < 0L); i++) {
	    p = InputData + (ptrdiff_t)k;
	    q = Kernel;
	    Sum = 0.0;
	    j = k - SignalLength;
	    if ((j + KernelLength) <= 0L) {
	      for (j = -KernelLength; (j < 0L); j++) {
		Sum += *p++ * *q--;
	      }
	    }
	    else {
	      while (j++ < 0L) {
		Sum += *p++ * *q--;
	      }
	      p = InputData;
	      m = 1L - (KernelLength + k) / SignalLength;
	      for (n = m; (n < 0L); n++) {
		for (j = -SignalLength; (j < 0L); j++) {
		  Sum += *p++ * *q--;
		}
		p = InputData;
	      }
	      for (j = (1L - m) * SignalLength - KernelLength - k; (j < 0L); j++) {
		Sum += *p++ * *q--;
	      }
	    }
	    if (++k == SignalLength) {
	      k = 0L;
	    }
	    *OutputData++ = Sum;
	  }
	  break;
	default:
	  Status = ERROR;
	  WRITE_ERROR(FirConvolve, "Invalid boundary convention")
	    break;
	}
  /**/DEBUG_WRITE_LEAVING(FirConvolve, "Done")
	return(Status);
} /* end FirConvolve */


int convolve_subsamp(double *x, int xn, double *y, int yn, double *k, int kn, 
		     int ofs, int shift)
/* convolves a signal x of length x with a kernel k of length k.
   first scalar product is computed at offset ofs, 
   i.e. sum(x[ofs..ofs+kn-1]*k[0..kn-1]), the next one at
   ofs+shift, etc., yn of them in total. The signal x is assumed to be
   zero outside the boundaries. */
{  
  int i,j,ik ;
  for (i=0,j=ofs;i<yn;i++,j+=shift) {
    y[i]=0.0 ;
    for (ik=max(-j,0);ik<min(kn,xn-j);ik++)
      y[i]+=k[ik]*x[j+ik] ;
  }
  return 0 ;
}

/*--------------------------------------------------------------------------*/


int convolve_upsample(double *x, int xn, double *y, 
			     double *k, int kn, int ko, int step) 
/* Convolves an upsampled version of x with a kernel k of length kn, */
/* with a center point ko. The result is stored into y of size
   (xn-1)*step+1. The signal x is assumed to be
   zero outside the boundaries. */
{
  int i,j,yn,isko ;
  yn=(xn-1)*step+1 ;
  for (i=0;i<yn;i++) y[i]=0.0 ;
  for(i=0;i<xn;i++) {
    isko=i*step-ko ; /* the first element of the kernel falls on y[isko] */
    for(j=max(0,-isko);j<min(kn,yn-isko);j++) 
      y[isko+j]+=x[i]*k[j] ;
  }
  return 0 ;
}

/*--------------------------------------------------------------------------*/
