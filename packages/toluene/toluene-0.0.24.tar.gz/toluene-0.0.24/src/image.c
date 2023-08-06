#include "image.h"

void tiled_tiff_decoder(int* data, int image_length, int image_width,
                        int tile_length, int tile_width, int bytes_per_channel,
                        int color_depth, int* outdata) {

    int pixel_size = bytes_per_channel*color_depth;
    int flattened_tile_size = tile_length*tile_width*pixel_size;
    int extra_tile_per_row = (image_width%tile_width > 0? 1 : 0);
    int tiles_per_row = image_width/tile_width + extra_tile_per_row;

    for(int y = 0; y < image_length; ++y) {
        for(int x = 0; x < image_width; ++x) {
            int tile_idx = x/tile_width + y/tile_length * tiles_per_row;

            int tile_pixel_idx = (x%tile_width + (y%tile_length)*tile_width)*pixel_size;
            int pixel_idx = tile_idx*flattened_tile_size + tile_pixel_idx;

            for(int color = 0; color < color_depth; ++color) {
                int value = 0;
                for(int byte = 0; byte < bytes_per_channel; ++byte){
                    value <<= 8;
                    value += data[pixel_idx+color*bytes_per_channel+byte];
                }
                outdata[(x+y*image_width)*color_depth+color] = value;
            }
        }
    }

}

void striped_tiff_decoder(int* data, int image_length, int image_width,
                          int bytes_per_channel, int color_depth,
                          int* outdata) {

    int pixel_size = bytes_per_channel*color_depth;
    int num_pixels = image_length*image_width;

    for(int i = 0; i < num_pixels*color_depth; ++i) {
        int value = 0;
        for(int byte = 0; byte < bytes_per_channel; ++byte){
            value <<= 8;
            value += data[i*pixel_size+byte];
        }
        outdata[i] = value;
    }

}
