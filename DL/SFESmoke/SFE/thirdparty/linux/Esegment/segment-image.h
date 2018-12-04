
/*
Copyright (C) 2006 Pedro Felzenszwalb

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
*/

#ifndef SEGMENT_IMAGE
#define SEGMENT_IMAGE

#include <set>
#include "segment-graph.h"
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

// dissimilarity measure between pixels
static inline double diff(Mat& img, int x1, int y1, int x2, int y2) {
    return  pow(img.at<char>(y1, x1) - img.at<char>(y2, x2), 2);
}

/*
 * Segment an image
 *
 * Returns a color image representing the segmentation.
 *
 * im: image to segment.
 * sigma: to smooth the image.
 * c: constant for treshold function.
 * min_size: minimum component size (enforced by post-processing stage).
 * num_ccs: number of connected components in the segmentation.
 */
void segment_image(Mat& im, double sigma, int c, int min_size, Mat& output) {
    Mat image;
    im.copyTo(image);

    int width = im.cols;
    int height = im.rows;

    GaussianBlur(image, image, Size(5, 5), sigma);

    // build graph
    edge *edges = new edge[width*height * 4];
    int num = 0;
    for (int y = 0; y < height - 1; y++) {
        for (int x = 0; x < width - 1; x++) {
            int a = y * width + x;
            int x2, y2;

            int arr[] = {
                x + 1, y,
                x, y + 1,
                x + 1,y + 1,
                x + 1,y - 1
            };

            int len = 8;
            if (y == 0) len -= 2;
            for (int i = 0; i < len; i += 2) {
                x2 = arr[i];
                y2 = arr[i + 1];
                edges[num].a = a;
                edges[num].b = y2 * width + x2;
                edges[num].w = diff(image, x, y, x2, y2);
                num++;
            }
        }
    }


    // segment
    universe *u = segment_graph(width*height, num, edges, c);

    // post process small components
    for (int i = 0; i < num; i++) {
        int a = u->find(edges[i].a);
        int b = u->find(edges[i].b);
        if ((a != b) && ((u->size(a) < min_size) || (u->size(b) < min_size)))
            u->join(a, b);
    }
    delete[] edges;


    im.copyTo(output);
    set<int> SET;
    int comp;

    for (int y = 0; y < height; y++) {
        comp = u->find(y * width + 0);
        SET.insert(comp);

        comp = u->find(y * width + width - 1);
        SET.insert(comp);
    }

    for (int x = 0; x < width; x++) {
        comp = u->find(x);
        SET.insert(comp);

        comp = u->find((height - 1) * width + x);
        SET.insert(comp);
    }

    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            comp = u->find(y * width + x);
            if (SET.find(comp) == SET.end())
                //output.at<Vec3b>(y, x) = Vec3b(0, 0, 0);
                output.at<char>(y, x) = 0;
        }
    }



    delete u;
}


#endif
