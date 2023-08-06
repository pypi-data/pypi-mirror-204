async def skelneckcoord():
    # Define the keypoints
    global total_pos
    
    
    keypoints = {
        0: 'nose',
        1: 'neck',
        2: 'right_shoulder',
        3: 'right_elbow',
        4: 'right_wrist',
        5: 'left_shoulder',
        6: 'left_elbow',
        7: 'left_wrist',
        8: 'right_hip',
        9: 'right_knee',
        10: 'right_ankle/foot',
        11: 'left_hip',
        12: 'left_knee',
        13: 'left_ankle/foot',
        14: 'right_eye',
        15: 'left_eye',
        16: 'right_ear',
        17: 'left_ear'
    }

    # Create ZED objects
    zed = sl.Camera()
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.sdk_verbose = True
    init_params.coordinate_units = sl.UNIT.MILLIMETER

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        # Quit if an error occurred
        exit()

    # Define the Object Detection module parameters
    obj_param = sl.ObjectDetectionParameters()
    # Different model can be chosen, optimizing the runtime or the accuracy
    obj_param.detection_model = sl.DETECTION_MODEL.HUMAN_BODY_FAST
    # run detection for every Camera grab
    obj_param.image_sync = True
    # Enable tracking to detect objects across time and space
    obj_param.enable_tracking = True
    # Optimize the person joints position, requires more computations
    obj_param.enable_body_fitting = True

    # If you want to have object tracking you need to enable positional tracking first
    if obj_param.enable_tracking:
        positional_tracking_param = sl.PositionalTrackingParameters()
        zed.enable_positional_tracking(positional_tracking_param)

    print("Object Detection: Loading Module...")
    err = zed.enable_object_detection(obj_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        zed.close()
        exit(1)

    # Set runtime parameter confidence to 40
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = 40

    objects = sl.Objects()
    j = 0
    # Grab new frames and detect objects
    while zed.grab() == sl.ERROR_CODE.SUCCESS:
        await asyncio.sleep(0.1)
        err = zed.retrieve_objects(objects, obj_runtime_param)
        if objects.is_new:
            # Count the number of objects detected
            obj_array = objects.object_list
            
            if len(obj_array) == 0:
                print("No people detected")
                global p 
                p = 1

            else:
                for i in range(len(obj_array)):
                    p = 0
                    print(f"Person {i+1} neck coordinates: ")
                    keypoint = obj_array[i].keypoint
                    neck_coordinates = keypoint[4]
                    nose_coordinates = keypoint[0]
                    bx = (nose_coordinates[0])/8
                    by = (nose_coordinates[1])/8
                    bz = nose_coordinates[2]
                    ax = (neck_coordinates[0])/8
                    ay = (neck_coordinates[1])/8
                    az = neck_coordinates[2]
                    
                    total_pos = [ax, ay,az]
                    if j % 5  == 0 :  
                        print(total_pos, end=', ')
                 
                    j = j + 1
                    # X is left right, y is up down (is POV is camera, right is negative), z is towards and away when facing

    # Disable object detection and close the camera
    zed.disable_object_detection()
    zed.close()
