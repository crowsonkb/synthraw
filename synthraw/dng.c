#include <stdint.h>
#include "tiffio.h"

TIFF* dng_open(char *path) {
    TIFF *tiff = TIFFOpen(path, "w");
    if (NULL == tiff) {
        return NULL;
    }

    static const uint16_t bayerPatternDimensions[] = {2, 2};
    static const float colorMatrix1[] = {
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0,
    };
    static const float asShotNeutral[] = {1.0, 1.0, 1.0};
    static const uint32_t blackLevel[] = {0};
    static const uint32_t whiteLevel[] = {65535};

    TIFFSetField(tiff, TIFFTAG_DNGVERSION, "\01\04\00\00");
    TIFFSetField(tiff, TIFFTAG_SUBFILETYPE, 0);
    TIFFSetField(tiff, TIFFTAG_COMPRESSION, COMPRESSION_NONE);
    TIFFSetField(tiff, TIFFTAG_BITSPERSAMPLE, 16);
    TIFFSetField(tiff, TIFFTAG_ROWSPERSTRIP, 1);
    TIFFSetField(tiff, TIFFTAG_ORIENTATION, ORIENTATION_TOPLEFT);
    TIFFSetField(tiff, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_CFA);
    TIFFSetField(tiff, TIFFTAG_SAMPLESPERPIXEL, 1);
    TIFFSetField(tiff, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
    TIFFSetField(tiff, TIFFTAG_SAMPLEFORMAT, SAMPLEFORMAT_UINT);
    TIFFSetField(tiff, TIFFTAG_CFAREPEATPATTERNDIM, bayerPatternDimensions);
    TIFFSetField(tiff, TIFFTAG_CFAPATTERN, "\00\01\01\02");
    TIFFSetField(tiff, TIFFTAG_MAKE, "synthraw");
    TIFFSetField(tiff, TIFFTAG_UNIQUECAMERAMODEL, "synthraw");
    TIFFSetField(tiff, TIFFTAG_COLORMATRIX1, 9, colorMatrix1);
    TIFFSetField(tiff, TIFFTAG_ASSHOTNEUTRAL, 3, asShotNeutral);
    TIFFSetField(tiff, TIFFTAG_CFALAYOUT, 1);
    TIFFSetField(tiff, TIFFTAG_CFAPLANECOLOR, 3, "\00\01\02");
    TIFFSetField(tiff, TIFFTAG_BLACKLEVEL, 1, blackLevel);
    TIFFSetField(tiff, TIFFTAG_WHITELEVEL, 1, whiteLevel);

    return tiff;
}

void dng_set_matrix(TIFF *tiff, float *matrix) {
    TIFFSetField(tiff, TIFFTAG_COLORMATRIX1, 9, matrix);
}

void dng_write_data(TIFF *tiff, uint16_t *data, size_t width, size_t height) {
    TIFFSetField(tiff, TIFFTAG_IMAGEWIDTH, width);
    TIFFSetField(tiff, TIFFTAG_IMAGELENGTH, height);

    uint16_t *cur = data;
    for (int row = 0; row < height; row++) {
        TIFFWriteScanline(tiff, cur, row, 0);
        cur += width;
    }
}

void dng_close(TIFF *tiff) {
    TIFFClose(tiff);
}
