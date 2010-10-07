/* Interpolation of a volume described by B-spline coefficients
   at arbitrary points.

   Jan Kybic, 1999
   $Id: splninterp.c,v 1.1 2005/10/07 15:45:06 eav Exp $
*/

#ifdef BIGSPLINES
#include "BIGsplines.h"
#include <math.h>
#include "Python.h"
#include "arrayobject.h"
#endif


extern int mfoldmirroronbound(int k,int n)
/* having a signal 0..n-1, fold k using mirror on boundary conditions, 
   i.e. k=n-1 gives n-1, k=n gives n-2, k=-1 gives 1 etc. */
{ int m;
  if (n<=1) return 0 ;
  m=2*(n-1) ;
  k=(k<0) ? k%m+m : k%m ;
  return k>=n ? m-k : k ;
}

extern double mfolddmirroronbound(double k,int n)
/* having a signal 0..n-1, fold k using mirror on boundary conditions, 
   i.e. k=n-1 gives n-1, k=n gives n-2, k=-1 gives 1 etc. */
{ double m, q;
  m=2*(n-1) ;
  q=floor(k/m) ; k-=q*m ;
  return k>n-1 ? m-k : k ;
}

extern int mfoldmirroroffbound(int k,int n)
/* having a signal 0..n-1, fold k using mirror off boundary conditions, 
   i.e. k=n-1 gives n-1, k=n gives n-1, k=-1 gives 0 etc. */
{ int m;
  if (n<=1) return 0 ;
  m=2*n ;
  k=(k<0) ? k%m+m : k%m ;
  return k>=n ? m-1-k : k ;
}

extern double mfolddmirroroffbound(double k,int n)
/* having a signal 0..n-1, fold k using mirror off boundary conditions, 
   i.e. k=n-1 gives n-1, k=n gives n-1, k=-1 gives 0 etc. */
{ double m, q;
  m=2*n ;
  q=floor(k/m) ; k-=q*m ;
  return k>n-1 ? m-1-k : k ;
}

extern int evalbspln(double *x,double *y, int n, int degree)
/* Evaluates B-spline of degree 'degree' at n-points x[0],...,x[n-1] */
/* results are put into y[0],..,y[n-1] */
{ int i,supp ;
  double (*evsplnx)(double) ;    /* pointer to the evaluation functions */
  if (choosespln(degree,&evsplnx,&supp,0)) {
    myErrMsg("Unsupported degree.") ;
    return 1 ;
  }

  for (i=0;i<n;i++) y[i]=(*evsplnx)(x[i]) ;
  return 0 ;
}


void dumpdata(const char * filename, void *data, int size) {
  FILE* f = fopen(filename, "wb");
  if (  f == NULL) {
    perror("unable to open file");
    exit(-1);
  }
  size_t s = fwrite(data, 1, size, f); 
  printf("dump size: %d\n", (int)s );
}

extern int splinterp
/* Takes an input matrix of size nxi*nyi*nzi, containing B-spline
   coefficients of degree `degree'. Samples the resulting function at
   nxc*nyc*nzc points given by coord, each point described by dims 
   coordinates. Uses mirror boundary conditions. Everything should be 
   allocated in advance.
   In this routine, x is simply the index that changes fastest and 
   z the index which changes slowest. C convention is applied for indexing,
   i.e. the first element of `input' is assumed to correspond to 
   point (0,0,0). If coord gives multidimensional coordinates, they are laid
   consecutively, i.e., as the fastest changing (sub)index - even faster 
   than x.
*/
(
	PyArrayObject	*coefsarray,					/* B-spline coefficients */
	PyArrayObject	*coordsarray,					/* 3D coordinates */
	PyArrayObject	*outputarray,				/* output values, one for each coord */
	int		degree,					/* 0 - Haar, 1 - Linear etc. */
	int		dflag,					/* 0 - value, 1,4,16 - first derivative with 
										respect to x,y,z ; 2,8,32 - second der. */
	int		bcond 
)
{
	double *input;
	double *coord;
	double *output;
	int ncoord;
	int	nxi, nyi;			/* input size */
	int nxc, nyc;			/* output size */ 
	int dims;				/* coordinate range dimensionality */
	int ix,iy,ofs,jx,jy,lx,ly;
	double (*evsplnx)(double);    /* pointer to the evaluation functions */
	double (*evsplny)(double);  
	int supp; double hsupp ;      /* spline support */
	double x,y,sum,sumt ;
	double *tabx,*taby,*ptr ;
	int *foldx,*foldy ;
	int (*mfold)(int,int) ; double (*mfoldd)(double,int) ;
	
	dims	= coefsarray->nd;
	ncoord	= coordsarray->nd;
	nxi		= coefsarray->dimensions[dims-1];
	nyi		= dims>1 ? coefsarray->dimensions[dims-2] : 1;
	nxc		= coordsarray->dimensions[ncoord-2];
	nyc		= ncoord>2 ? coordsarray->dimensions[ncoord-3] : 1;
	
	input	= (double *)coefsarray->data;
	coord	= (double *)coordsarray->data;
	output	= (double *)outputarray->data;
	
	switch(bcond) {
	case MirrorOffBounds: 
		mfold=mfoldmirroroffbound ;
		mfoldd=mfolddmirroroffbound ;
		break ;
	case MirrorOnBounds: 
		mfold=mfoldmirroronbound ;
		mfoldd=mfolddmirroronbound ;
		break ;
	default:
		myErrMsg("Unsupported boundary conditions.") ;
		return 1 ;
	}

	//printf("splninterp called with nxi=%d nyi=%d nxc=%d nyc=%d dims=%d degree=%d, dflag=%d bcond=%d\n", nxi, nyi, nxc, nyc, dims, degree,dflag, bcond) ;
	//dumpdata("input.raw", (void*)input, sizeof(double)*nxi*nyi);
	//dumpdata("coord.raw", (void*)coord, sizeof(double)*nxi*nyi);
	//dumpdata("output.raw", (void*)coord, sizeof(double)*nxc*nyc);

	if (choosespln(degree,&evsplnx,&supp,dflag & 3) | 
		choosespln(degree,&evsplny,NULL,(dflag & 12)>>2)) 
	{
		myErrMsg("Unsupported degree,dflag.") ;
		return 1 ;
	}
	hsupp=supp/2.0 ;

	/* normal case */	
	myMalloc(tabx,supp,1)
	myMalloc(taby,supp,1);
	myMallocInt(foldx,supp,1); 
	myMallocInt(foldy,supp,1) ;

	for (iy=0;iy<nyc;iy++)/* loop through all elements of coord */
	for (ix=0;ix<nxc;ix++) 
	{
		ofs	= dims*(ix+nxc*(iy)) ;
		x	= coord[ofs] ;
		y	= dims > 1 ? coord[ofs+1] : 0.0 ;
		lx	= ceil(x-hsupp);
		ly	= ceil(y-hsupp);
		sum	= 0.0 ;
		/* precalculate B-spline values and folded indexes */
		for(jx=0;jx<supp;jx++) 
		{
			tabx[jx]=(*evsplnx)(x-jx-lx); 
			foldx[jx]=mfold(jx+lx,nxi);
		}
		/* 2D case */
		for (jy=ly;jy<ly+supp;jy++) 
		{
			ptr=input+nxi*mfold(jy,nyi);
			for (sumt=0.0,jx=0;jx<supp;jx++) 
			{
				sumt+=ptr[foldx[jx]]*tabx[jx];
			}
			sum+=sumt*(*evsplny)(y-jy) ;
			output[ix+nxc*(iy)]=sum ;
		} /* for ix */
	}
	myFree(tabx);
	myFree(taby);
	myFree(foldx);
	myFree(foldy);
	//exit(-1);
	return 0 ;
}
