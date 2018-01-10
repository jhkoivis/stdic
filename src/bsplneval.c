/* Evaluate B-splines of various degrees and their derivatives    

   $Id
   Jan Kybic, 1999
*/

#ifdef BIGSPLINES
#include "BIGsplines.h"
#include <math.h>
#endif


double bspln3(double x) /* cubic */
{ 
  x=fabs(x) ;
  if (x>2.0) return 0.0 ;
  if (x>1.0) return (2.0-x)*(2.0-x)*(2.0-x)/6.0 ;
  return 2.0/3.0-x*x*(1-0.5*x) ;
}

double bspln2(double x) /* quadratic */
{ 
  x=fabs(x) ;
  if (x>1.5) return 0.0 ;
  if (x>0.5) return (1.5-x)*(1.5-x)/2.0 ;
  return 0.75-x*x ;
}

double bspln2d(double x) /* quadratic, derivative */
{ double xa ;
  xa=fabs(x) ;
  if (xa>1.5) return 0.0 ;
  if (xa>0.5) return (x>0.0) ? xa-1.5 : 1.5-xa ;
  return -2.0*x ;
}

double bspln2dd(double x) /* quadratic, second derivative */
{ 
  if (x>0.0) {
    if (x>1.5) return 0.0 ;
    if (x>0.5) return 1.0 ; else return -2.0 ;
  } else {
    if (x<-1.5) return 0.0 ;
    if (x<-0.5) return 1.0 ; else return -2.0 ;
  } 
}

double bspln1(double x) /* linear */
{ 
  x=fabs(x) ;
  if (x>1.0) return 0.0 ;
  return 1.0-x ;
}

double bspln0(double x) /* Haar */
{ 
  x=fabs(x) ;
  if (x>0.5) return 0.0 ;
  return 1.0 ;
}

double bspln1d(double x) /* linear, derivative */
{ 
  if (fabs(x)>1.0) return 0.0 ;
  if (x>0.0) return -1.0 ; else return 1.0 ;
}
  
double bspln3d(double x) /* cubic, derivative */
{ double y ;

  y=x>0.0 ? 1.0 : -1.0 ;
  x=fabs(x) ;
  if (x>2) return 0.0 ;
  if (x>1) return -0.5*y*(2-x)*(2-x) ;
  return (1.5*x-2)*x*y ;
}

double bspln3dd(double x) /* cubic, second derivative */
{ 
  x=fabs(x) ;
  if (x>2.0) return 0.0 ;
  if (x>1.0) return 2.0-x ;
  return 3.0*x-2.0 ;
}

int choosespln(int degree,double (**fp)(double),int *sp,int type)
     /* type 0 - value, 1 - deriv. , 2 - dderiv */
{
  if (sp) *sp=1+degree ; 
  if (!fp || type<0 || type>2) return -1 ;
  *fp=NULL ;
  switch(degree) {
  case 0: *fp= type==0 ? bspln0 : NULL ; break ;
  case 1: *fp= type==0 ? bspln1 : ( type==1 ? bspln1d : NULL ) ; break ;
  case 2: *fp= type==0 ? bspln2 : ( type==1 ? bspln2d : bspln2dd ) ; break ;
  case 3: *fp= type==0 ? bspln3 : ( type==1 ? bspln3d : bspln3dd ) ; break ;
  default: return -1 ;
  }
  if (!(*fp)) return -1 ;
  return 0 ;
} 
