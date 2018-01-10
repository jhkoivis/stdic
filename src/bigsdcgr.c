/* This is bigsdcgr.c to evaluate fast the criterion and gradient
   as bigregister.getEg()

   Jan Kybic, 1999-January 2001

   part of NumericPython BIGsplines toolbox
   $Id: bigsdcgr.c,v 1.1 2005/10/07 15:45:06 eav Exp $

   Usage:

   Only works for 2D. Use Python/Fortran (not Matlab) ordering of images.

*/

#include <math.h>
#include "BIGsplines.h" 

int bigsdcgr(double *fr,  /* reference image */
	      double *E,   /* the criterion value */
	      double *gr,  /* the gradient */
	      int degc,  /* degree for the coefficients */
	      int frx, int fry, /* size of the reference image */
	      int cx, int cy,    /* size of the image coefficients */
	      double *derw, /* first derivatives */
	      double *fw   /* warped test image */
	      )
{
  double e ; 
  int ix,iy ; int cnum,imcnt ;
  double shift,stepx,stepy,hsupp ;
  double parx,pary ;
  double *derx,*dery ;
  int lowx,lowy,highx,highy ;
  int supp,ind1,ind2,ind3,ind4 ;
  int jx,jy,jxf,jyf ;
  int cnd,cxe,cye ;
  double *tabx,*taby ;
  double ederx ;
  double edery ;
  double betajy,betajxjy ;
  double (*evspln)(double) ;    /* pointer to the evaluation function */

  int (*mfold)(int,int) ; double (*mfoldd)(double,int) ;
  /* for the moment, enforce mirror-off-bound condition */
  mfold=mfoldmirroroffbound ; 
  mfoldd=mfolddmirroroffbound ;


  /* printf("frx=%d fry=%d cx=%d cy=%d degc=%d\n",frx,fry,cx,cy,degc) ; 
   */

  if (choosespln(degc,&evspln,&supp,0)) myErrMsg("Unsupported degc") ;

  hsupp=supp/2.0 ;
  shift=0.0 ; /* we now put the basis function in the corners */
  stepx=(cx-1)/((double)frx-1) ; stepy=(cy-1)/((double)fry-1) ; 
  
  /* printf("stepx=%f stepy=%f\n",stepx,stepy) ;
   */

  cnum=cx*cy ;
  cnd=cnum*2 ; /* 2 is the number of dimensions */
  imcnt=frx*fry ;
  derx=derw ; dery=derx+imcnt ;

  /* zero E and gr */
  for(ix=0;ix<cnd;ix++) gr[ix]=0.0 ;
  *E=0.0 ; 

  /* allocate and precalculate tabx, taby */
  cxe=cx+2*supp ;/* 2*supp is too much but who cares... */
  myMalloc(tabx,cxe,frx) ; 
  for(ix=0;ix<frx;ix++) { 
  	  parx=shift+stepx*ix ; 
	  lowx=(int)floor(parx-hsupp) ; highx=lowx+supp ;
	  for(jx=lowx;jx<=highx;jx++)
	    tabx[ix*cxe+supp+jx]=(*evspln)(parx-jx) ;
  }
  cye=cy+2*supp ;/* 2*supp is too much but who cares... */
  myMalloc(taby,cye,fry) ; 
  for(iy=0;iy<fry;iy++) { 
  	  pary=shift+stepy*iy ; 
	  lowy=(int)floor(pary-hsupp) ; highy=lowy+supp ;
	  for(jy=lowy;jy<=highy;jy++)
	    taby[iy*cye+supp+jy]=(*evspln)(pary-jy) ;
  }
  

  /* 2D case gradient and Hessian calculation starts here */
  for(iy=0;iy<fry;iy++) { /* loop through all pixels */
        pary=shift+stepy*iy ;
	ind4=iy*cye+supp ;
	lowy=(int)floor(pary-hsupp) ; highy=lowy+supp ;
	/*printf("iy=%d pary=%f pary-hsupp=%f lowy=%d highy=%d\n",
	  iy,pary,pary-hsupp,lowy,highy) ;*/
	for(ix=0;ix<frx;ix++) { 
	  ind1=ix+frx*iy ;
	  ind3=ix*cxe+supp ;
	  e=fw[ind1]-fr[ind1] ;
	  (*E)+=e*e ;
	  /* calculate the range of influential parameters */
	  parx=shift+stepx*ix ; 
	  lowx=(int)floor(parx-hsupp) ; highx=lowx+supp ;
	  ederx=2.0*e*derx[ind1] ;
	  edery=2.0*e*dery[ind1] ;
	  /* precalculate tabx */
	  for(jy=lowy;jy<=highy;jy++) { /* loop through influential c's */
	    betajy=taby[ind4+jy] ;
	    jyf=mfold(jy,cy) ;
	    /* printf("mfold(%d,%d)=%d ",jy,cy,jyf) ; */
	    for(jx=lowx;jx<=highx;jx++) { 
	      betajxjy=tabx[ind3+jx]*betajy ;
	      jxf=mfold(jx,cx) ;
	      ind2=jxf+cx*jyf ;
	      gr[ind2]+=betajxjy*ederx ;
	      gr[ind2+cnum]+=betajxjy*edery ;
	    } /* for jx */
	  } /* for jy */
	} /* for ix */
      } /* for iy */
  myFree(tabx) ;
  myFree(taby) ;
  return 0 ;
}

/* end of bigsdcgr */

/* -------------------------------------------------------------------- */

int bigsdcgrmask(double *fr,  /* reference image */
	      double *E,   /* the criterion value */
	      double *gr,  /* the gradient */
	      int degc,  /* degree for the coefficients */
	      int frx, int fry, /* size of the reference image */
	      int cx, int cy,    /* size of the image coefficients */
	      double *derw, /* first derivatives */
	      double *fw,   /* warped test image */
	      unsigned char *mask /* mask, if zero, ignore pixel */	 
	      )
{
  double e ; 
  int ix,iy ; int cnum,imcnt ;
  double shift,stepx,stepy,hsupp ;
  double parx,pary ;
  double *derx,*dery ;
  int lowx,lowy,highx,highy ;
  int supp,ind1,ind2,ind3,ind4 ;
  int jx,jy,jxf,jyf ;
  int cnd,cxe,cye ;
  double *tabx,*taby ;
  double ederx ;
  double edery ;
  double betajy,betajxjy ;
  double (*evspln)(double) ;    /* pointer to the evaluation function */

  int (*mfold)(int,int) ; double (*mfoldd)(double,int) ;
  /* for the moment, enforce mirror-off-bound condition */
  mfold=mfoldmirroroffbound ; 
  mfoldd=mfolddmirroroffbound ;

  /* printf("frx=%d fry=%d cx=%d cy=%d degc=%d\n",frx,fry,cx,cy,degc) ; 
   */

  if (choosespln(degc,&evspln,&supp,0)) myErrMsg("Unsupported degc") ;

  hsupp=supp/2.0 ;
  shift=0.0 ; /* we now put the basis function in the corners */
  stepx=(cx-1)/((double)frx-1) ; stepy=(cy-1)/((double)fry-1) ; 
  
  /* printf("stepx=%f stepy=%f\n",stepx,stepy) ;
   */

  cnum=cx*cy ;
  cnd=cnum*2 ; /* 2 is the number of dimensions */
  imcnt=frx*fry ;
  derx=derw ; dery=derx+imcnt ;

  /* zero E and gr */
  for(ix=0;ix<cnd;ix++) gr[ix]=0.0 ;
  *E=0.0 ; 

  /* allocate and precalculate tabx, taby */
  cxe=cx+2*supp ;/* 2*supp is too much but who cares... */
  myMalloc(tabx,cxe,frx) ; 
  for(ix=0;ix<frx;ix++) { 
  	  parx=shift+stepx*ix ; 
	  lowx=(int)floor(parx-hsupp) ; highx=lowx+supp ;
	  for(jx=lowx;jx<=highx;jx++)
	    tabx[ix*cxe+supp+jx]=(*evspln)(parx-jx) ;
  }
  cye=cy+2*supp ;/* 2*supp is too much but who cares... */
  myMalloc(taby,cye,fry) ; 
  for(iy=0;iy<fry;iy++) { 
  	  pary=shift+stepy*iy ; 
	  lowy=(int)floor(pary-hsupp) ; highy=lowy+supp ;
	  for(jy=lowy;jy<=highy;jy++)
	    taby[iy*cye+supp+jy]=(*evspln)(pary-jy) ;
  }
  

  /* 2D case gradient and Hessian calculation starts here */
  for(iy=0;iy<fry;iy++) { /* loop through all pixels */
        pary=shift+stepy*iy ;
	ind4=iy*cye+supp ;
	lowy=(int)floor(pary-hsupp) ; highy=lowy+supp ;
	/*printf("iy=%d pary=%f pary-hsupp=%f lowy=%d highy=%d\n",
	  iy,pary,pary-hsupp,lowy,highy) ;*/
	for(ix=0;ix<frx;ix++) { 
	  ind1=ix+frx*iy ;
	  if (!mask[ind1]) continue ; /* skip pixel for zero mask */
	  ind3=ix*cxe+supp ;
	  e=fw[ind1]-fr[ind1] ;
	  (*E)+=e*e ;
	  /* calculate the range of influential parameters */
	  parx=shift+stepx*ix ; 
	  lowx=(int)floor(parx-hsupp) ; highx=lowx+supp ;
	  ederx=2.0*e*derx[ind1] ;
	  edery=2.0*e*dery[ind1] ;
	  /* precalculate tabx */
	  for(jy=lowy;jy<=highy;jy++) { /* loop through influential c's */
	    betajy=taby[ind4+jy] ;
	    jyf=mfold(jy,cy) ;
	    /* printf("mfold(%d,%d)=%d ",jy,cy,jyf) ; */
	    for(jx=lowx;jx<=highx;jx++) { 
	      betajxjy=tabx[ind3+jx]*betajy ;
	      jxf=mfold(jx,cx) ;
	      ind2=jxf+cx*jyf ;
	      gr[ind2]+=betajxjy*ederx ;
	      gr[ind2+cnum]+=betajxjy*edery ;
	    } /* for jx */
	  } /* for jy */
	} /* for ix */
      } /* for iy */
  myFree(tabx) ;
  return 0 ;
}

/* end of bigsdcgr */
