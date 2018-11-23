#include <opencv2/opencv.hpp>
#include "segment-image.h"

int main(int argc, char* argv[]) {
    if (argc != 5)
        printf("arguments: filename, sigma, c, min_size\n");
    else {
        Mat img = imread(argv[1], 0);
        Mat img2;

        double sigma = atof(argv[2]);
        int c = atoi(argv[3]);
        int min_size = atoi(argv[4]);

        clock_t t = clock();
        segment_image(img, sigma, c, min_size, img2);
        double t2 = (double)(clock() - t) / CLOCKS_PER_SEC;
        printf("%f\n", t2);

        imshow("source", img);
        imshow("result", img2);
        waitKey();
        destroyAllWindows();
    }
}