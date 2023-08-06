#ifndef _AXDL_H_
#define _AXDL_H_

#ifdef __cplusplus
extern "C"
{
#endif

#define SAMPLE_MAX_BBOX_COUNT 64
#define SAMPLE_MAX_FACE_BBOX_COUNT 64
#define SAMPLE_MAX_YOLOV5_MASK_OBJ_COUNT 8
#define SAMPLE_MAX_POSE_COUNT 3
#define SAMPLE_OBJ_NAME_MAX_LEN 20
#define SAMPLE_MAX_HAND_BBOX_COUNT 2
#define SAMPLE_RINGBUFFER_CACHE_COUNT 8
#define SAMPLE_FACE_FEAT_LEN 512
    typedef enum _MODEL_TYPE_E
    {
        MT_UNKNOWN = -1,

        // detection
        MT_DET = 0x10000,
        MT_DET_YOLOV5,
        MT_DET_YOLOV5_FACE,
        MT_DET_YOLOV5_LICENSE_PLATE,
        MT_DET_YOLOV6,
        MT_DET_YOLOV7,
        MT_DET_YOLOV7_FACE,
        MT_DET_YOLOV7_PALM_HAND,
        MT_DET_YOLOX,
        MT_DET_NANODET,
        MT_DET_YOLOX_PPL,
        MT_DET_PALM_HAND,
        MT_DET_YOLOPV2,
        MT_DET_YOLO_FASTBODY,
        MT_DET_SCRFD,
        MT_DET_YOLOV8,
        MT_DET_YOLOV8_SEG,
        MT_DET_CROWD_COUNT,

        // segmentation
        MT_SEG = 0x20000,
        MT_SEG_PPHUMSEG,

        // instance segmentation
        MT_INSEG = 0x30000,
        MT_INSEG_YOLOV5_MASK,

        // multi level model
        MT_MLM = 0x40000,
        MT_MLM_HUMAN_POSE_AXPPL,
        MT_MLM_HUMAN_POSE_HRNET,
        MT_MLM_ANIMAL_POSE_HRNET,
        MT_MLM_HAND_POSE,
        MT_MLM_FACE_RECOGNITION,
        MT_MLM_VEHICLE_LICENSE_RECOGNITION,

    } MODEL_TYPE_E;

    typedef struct _bbox_t
    {
        float x, y, w, h;
    } axdl_bbox_t;

    typedef struct _point_t
    {
        float x, y;
    } axdl_point_t;

    typedef struct _mat_t
    {
        int w, h;
        unsigned char *data;
    } axdl_mat_t;

    typedef struct _object_t
    {
        axdl_bbox_t bbox;
        int bHasBoxVertices; // bbox with rotate
        axdl_point_t bbox_vertices[4];

        int nLandmark; // num of lmk
#define SAMPLE_PLATE_LMK_SIZE 4
#define SAMPLE_FACE_LMK_SIZE 5
#define SAMPLE_BODY_LMK_SIZE 17
#define SAMPLE_ANIMAL_LMK_SIZE 20
#define SAMPLE_HAND_LMK_SIZE 21
        axdl_point_t *landmark;

        int bHasMask;
        axdl_mat_t mYolov5Mask; // cv::Mat

        int bHasFaceFeat;
        axdl_mat_t mFaceFeat;

        int label;
        float prob;
        char objname[SAMPLE_OBJ_NAME_MAX_LEN];
    } axdl_object_t;

    typedef struct _results_t
    {
        int mModelType; // MODEL_TYPE_E
        int nObjSize;
        axdl_object_t mObjects[SAMPLE_MAX_BBOX_COUNT];

        int bPPHumSeg;
        axdl_mat_t mPPHumSeg;

        int bYolopv2Mask;
        axdl_mat_t mYolopv2seg;
        axdl_mat_t mYolopv2ll;

        int nCrowdCount;
        axdl_point_t *mCrowdCountPts;

        int niFps /*inference*/, noFps /*osd*/;

    } axdl_results_t;

    typedef struct _canvas_t
    {
        unsigned char *data;
        int width, height, channel;
    } axdl_canvas_t;

    typedef enum _color_space_e
    {
        axdl_color_space_unknown,
        axdl_color_space_nv12,
        axdl_color_space_nv21,
        axdl_color_space_bgr,
        axdl_color_space_rgb,
    } axdl_color_space_e;

    typedef struct _image_t
    {
        unsigned long long int pPhy;
        void *pVir;
        unsigned int nSize;
        unsigned int nWidth;
        unsigned int nHeight;
        axdl_color_space_e eDtype;
        union
        {
            int tStride_H, tStride_W, tStride_C;
        };
    } axdl_image_t;

    int axdl_parse_param_init(char *json_file_path, void **pModels);
    void axdl_deinit(void **pModels);

    int axdl_get_ivps_width_height(void *pModels, char *json_file_path, int *width_ivps, int *height_ivps);
    axdl_color_space_e axdl_get_color_space(void *pModels);
    int axdl_get_model_type(void *pModels);

    int axdl_inference(void *pModels, axdl_image_t *pstFrame, axdl_results_t *pResults);

    int axdl_draw_results(void *pModels, axdl_canvas_t *canvas, axdl_results_t *pResults, float fontscale, int thickness, int offset_x, int offset_y);
#ifdef __cplusplus
}
#endif

#endif