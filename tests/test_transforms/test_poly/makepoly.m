
refI  = imread('../refimg.png');
testI = imread('../testimg.png');

refIc = refI(1:750,1:250);
imwrite(refIc, 'img-00.tiff', 'tiff');

xybase = rand(6,2);

T1 = [0                                        0
      1                                        0
      0                                        1
      -1.2454075596238809e-05 -2.10659363809e-05
      0                                        0
      0                                        0];

T2 = [0                                        0
      1                                        0
      0                                        1
      -2.4663953631767257e-05 -4.17188151856e-05
      0                                        0
      0                                        0];

T3 = [0                                        0
      1                                        0
      0                                        1
      -3.6636746656896907e-05 -6.19706672175e-05
      0                                        0
      0                                        0];
 
T4 = [0                                        0
      1                                        0
      0                                        1
      -4.8379293662312578e-05 -8.18330605565e-05
      0                                        0
      0                                        0];

T5 = [0                                        0
      1                                        0
      0                                        1
      -5.9898173105720345e-05 -0.000101317122594
      0                                        0
      0                                        0];
  
for i=1:5;
    tform = cp2tform(xybase, xybase, 'polynomial', 2);
    tform.tdata = eval(sprintf('T%d',i));
    testIt = imtransform(testI, tform);
    testItc = testIt(1:750,1:250);
    imwrite(testItc, sprintf('img-%02d.tiff',i), 'tiff');
end;