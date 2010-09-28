
refI  = imread('../refimg.png');
testI = imread('../testimg.png');

refIc = refI(1:750,1:250);
imwrite(refIc, 'img-00.tiff', 'tiff');

for i=1:5;
    
    strain    = i/100 + 1;
    transform = maketform('affine', [1 0 0; 0 strain 0; 0 0 1]);
    testIt    = imtransform(testI, transform);
    testItc   = testIt(1:750,1:250);
    imwrite(testItc, sprintf('img-%02d.tiff',i), 'tiff');
    
end;