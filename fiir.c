/* This is fiir.c, a IIR filtering routine by Philippe Thevenaz
   Modified by Jan Kybic, August 2000

   part of NumericPython BIGsplines toolbox
   $Id: fiir.c,v 1.1 2005/10/07 15:45:06 eav Exp $

   Usage:

	IirConvolvePoles(x,y,nx,zi,nz,MirrorOnBounds,1e-20) ;

   where 1e-20 is the tolerance, x the input, y output, zi poles,
   nz the number of poles
   
*/

#include <math.h>
#include "BIGsplines.h"

/*--------------------------------------------------------------------------*/

static double PositiveIntPower(double x,int n)
{
  double y=1.0 ;
  while (n--) y*=x ;
  return y;
}

static long ConvertDoubleToLong(double x) { return (long)x ; }

extern int		IirConvolvePoles
(
 double	InputData[],		/* data to process */
 double	OutputData[],		/* result */
 long	SignalLength,		/* length of the 1D data array */
 double	RealPoles[],		/* array of real poles */
 long	PoleNumber,			/* number of poles */
 enum TBoundaryConvention
 Convention,			/* boundary convention */
 double	Tolerance			/* admissible relative error */
 )

     /* the input and the output have the same length */
     /* in-place processing is allowed */
     /* no more than two poles are allowed for a finite support boundary */
     /* success: return(!ERROR); failure: return(ERROR) */

{ /* begin IirConvolvePoles */

  double	*p, *q;
  double	Sum, Gain;
  double	z, z0, z1, z2, iz;
  long	Horizon;
  long	i, j;
  int		Status = !ERROR;
  
  Gain = 1.0;
  for (i = 0L; (i < PoleNumber); i++) {
    z = RealPoles[i];
    if (0.0 <= z) {
      Status = ERROR;
      WRITE_ERROR(IirConvolvePoles,
		  "Invalid pole (should be strictly negative)")
	return(Status);
    }
    z1 = 1.0 - z;
    Gain *= -(z1 * z1) / z;
  }
  p = InputData;
  q = OutputData;
  for (i = -SignalLength; (i < 0L); i++) {
    *q++ = *p++ * Gain;
  }
  switch (Convention) {
  case AntiMirrorOnBounds:
    if (SignalLength == 1L) {
      *OutputData = *InputData;
      return(Status);
    }
    for (i = 0L; (i < PoleNumber); i++) {
      z = RealPoles[i];
      Sum = ((1.0 + z) / (1.0 - z)) * (OutputData[0]
				       - PositiveIntPower(z, SignalLength - 1L) 
				       * OutputData[SignalLength - 1L]);
      z1 = z;
      z2 = PositiveIntPower(z, 2L * SignalLength - 3L);
      iz = 1.0 / z;
      for (j = 1L; (j < (SignalLength - 1L)); j++) {
	Sum += (z2 - z1) * OutputData[j];
	z1 *= z;
	z2 *= iz;
      }
      OutputData[0] = Sum / (1.0 - 
			     PositiveIntPower(z, 2L * SignalLength - 2L));
      for (j = 1L; (j < SignalLength); j++) {
	OutputData[j] += z * OutputData[j - 1L];
      }
      OutputData[SignalLength - 1L] = (-z / ((1.0 - z) * (1.0 - z)))
	* (OutputData[SignalLength - 1L] 
	   - z * OutputData[SignalLength - 2L]);
      for (j = SignalLength - 2L; (0L <= j); j--) {
	OutputData[j] = z * (OutputData[j + 1L] - OutputData[j]);
      }
    }
    break;
  case FiniteCoefficientSupport:
    switch (PoleNumber) {
    case 1L:
      z = RealPoles[0];
      Sum = (OutputData[0] - PositiveIntPower(z, SignalLength + 1L)
	     * OutputData[SignalLength - 1L]) * (1.0 + z) / (z * z);
      z1 = z;
      z2 = PositiveIntPower(z, 2L * SignalLength - 2L);
      iz = 1.0 / z;
      for (j = 1L; (j < (SignalLength - 1L)); j++) {
	Sum -= (z2 + z1) * OutputData[j];
	z1 *= z;
	z2 *= iz;
      }
      OutputData[0] = Sum / ((1.0 + z) * ((1.0 + z * z
         + PositiveIntPower(z, 2L * SignalLength)) / (z * z)
         + (z * z - PositiveIntPower(z, SignalLength)) / (1.0 - z)));
      for (j = 1L; (j < SignalLength); j++) {
	OutputData[j] += z * OutputData[j - 1L];
      }
      OutputData[SignalLength - 1L] *= -z;
      for (j = SignalLength - 2L; (0L <= j); j--) {
	OutputData[j] = z * (OutputData[j + 1L] - OutputData[j]);
      }
      break;
    default:
      Status = ERROR;
      WRITE_ERROR(IirConvolvePoles,
        "Invalid number of poles (should be 1 for FiniteCoefficientSupport)")
	break;
    }
    break;
  case FiniteDataSupport:
    switch (PoleNumber) {
    case 1L:
      z = RealPoles[0];
      for (j = 1L; (j < SignalLength); j++) {
	OutputData[j] += z * OutputData[j - 1L];
      }
      OutputData[SignalLength - 1L] *= z / (z * z - 1.0);
      for (j = SignalLength - 2L; (0L <= j); j--) {
	OutputData[j] = z * (OutputData[j + 1L] - OutputData[j]);
      }
      break;
    case 2L:
      z0 = RealPoles[0];
      for (j = 1L; (j < SignalLength); j++) {
	OutputData[j] += z0 * OutputData[j - 1L];
      }
      OutputData[SignalLength - 1L] *= z0 / (z0 * z0 - 1.0);
      z = OutputData[SignalLength - 1L];
      for (j = SignalLength - 2L; (0L <= j); j--) {
	OutputData[j] = z0 * (OutputData[j + 1L] - OutputData[j]);
      }
      z1 = RealPoles[1];
      OutputData[0] /= 1.0 - z0 * z1;
      for (j = 1L; (j < SignalLength); j++) {
	OutputData[j] += z1 * OutputData[j - 1L];
      }
      OutputData[SignalLength - 1L] = (z1 / (z1 * z1 - 1.0))
	* (OutputData[SignalLength - 1L] - (z0 * z1 / (z0 * z1 - 1.0)) * z);
      for (j = SignalLength - 2L; (0L <= j); j--) {
	OutputData[j] = z1 * (OutputData[j + 1L] - OutputData[j]);
      }
      break;
    default:
      Status = ERROR;
      WRITE_ERROR(IirConvolvePoles,
       "Invalid number of poles (should be 1 or 2 for FiniteDataSupport)")
	break;
    }
    break;
  case MirrorOffBounds:
    if (SignalLength == 1L) {
      *OutputData = *InputData;
      return(Status);
    }
    for (i = 0L; (i < PoleNumber); i++) {
      z = RealPoles[i];
      Sum = (OutputData[0] + PositiveIntPower(z, SignalLength)
	     * OutputData[SignalLength - 1L]) * (1.0 + z) / z;
      z1 = z;
      z2 = PositiveIntPower(z, 2L * SignalLength - 2L);
      iz = 1.0 / z;
      for (j = 1L; (j < (SignalLength - 1L)); j++) {
	Sum += (z2 + z1) * OutputData[j];
	z1 *= z;
	z2 *= iz;
      }
      OutputData[0] = Sum * z / (1.0 - PositiveIntPower(z, 2L * SignalLength));
      for (j = 1L; (j < SignalLength); j++) {
	OutputData[j] += z * OutputData[j - 1L];
      }
      OutputData[SignalLength - 1L] *= z / (z - 1.0);
      for (j = SignalLength - 2L; (0L <= j); j--) {
	OutputData[j] = z * (OutputData[j + 1L] - OutputData[j]);
      }
    }
    break;
  case MirrorOnBounds:
    if (SignalLength == 1L) { *OutputData = *InputData;
			      return(Status);
    }
    for (i = 0L; (i < PoleNumber); i++) {
      z = *RealPoles++;
      if (Tolerance == 0.0) {
	Horizon = SignalLength;
      }
      else {
	Horizon = ConvertDoubleToLong(ceil(log(Tolerance) / log(fabs(z))));
      }
      if (Horizon < SignalLength) {
	z1 = z;
	Sum = *OutputData;
	p = OutputData;
	for (j = -Horizon; (j < 0L); j++) {
	  Sum += z1 * *++p;
	  z1 *= z;
	}
	p = OutputData;
	q = OutputData;
	*p++ = Sum;
	for (j = 1L - SignalLength; (j < 0L); j++) {
	  *p++ += z * *q++;
	}
	p = q--;
	*p = (z * *q + *p) * z / (z * z - 1.0);
	for (j = SignalLength - 2L; (0L <= j); j--) {
	  *q-- = z * (*p-- - *q);
	}
      }
      else {
	z1 = z;
	z2 = PositiveIntPower(z, SignalLength - 1L);
	iz = 1.0 / z;
	Sum = *OutputData + z2 * OutputData[SignalLength - 1L];
	z2 *= z2 * iz;
	p = OutputData;
	for (j = 2L - SignalLength; (j < 0L); j++) {
	  Sum += (z1 + z2) * *++p;
	  z1 *= z;
	  z2 *= iz;
	}
	p = OutputData;
	q = OutputData;
	*p++ = Sum / (1.0 - z2 * z2);
	for (j = 1L - SignalLength; (j < 0L); j++) {
	  *p++ += z * *q++;
	}
	p = q--;
	*p = (z * *q + *p) * z / (z * z - 1.0);
	for (j = SignalLength - 2L; (0L <= j); j--) {
	  *q-- = z * (*p-- - *q);
	}
      }
    }
    break;
  case Periodic:
    if (SignalLength == 1L) {
      *OutputData = *InputData;
      return(Status);
    }
    for (i = 0L; (i < PoleNumber); i++) {
      z = RealPoles[i];
      z2 = PositiveIntPower(z, SignalLength - 1L);
      iz = 1.0 / z;
      Sum = OutputData[0];
      for (j = 1L; (j < SignalLength); j++) {
	Sum += z2 * OutputData[j];
	z2 *= iz;
      }
      OutputData[0] = Sum / (1.0 - PositiveIntPower(z, SignalLength));
      for (j = 1L; (j < SignalLength); j++) {
	OutputData[j] += z * OutputData[j - 1L];
      }
      Sum = OutputData[0] + OutputData[SignalLength - 1L] / z;
      z1 = z;
      for (j = 1L; (j < (SignalLength - 1L)); j++) {
	Sum += z1 * OutputData[j];
	z1 *= z;
      }
      OutputData[SignalLength - 1L] = Sum * z * z
	/ (PositiveIntPower(z, SignalLength) - 1.0);
      for (j = SignalLength - 2L; (0L <= j); j--) {
	OutputData[j] = z * (OutputData[j + 1L] - OutputData[j]);
      }
    }
    break;
  default:
    Status = ERROR;
    WRITE_ERROR(IirConvolvePoles,"Invalid boundary convention")
      break;
  }
  return(Status);
} /* end IirConvolvePoles */


/*--------------------------------------------------------------------------*/


