# 优化器配置
optimizer = dict(type='SGD', lr=0.01,  weight_decay=5e-4, momentum=0.9, nesterov=True)
optimizer_config = dict(grad_clip=dict(max_norm=20))

# 学习率调度配置
lr_config = dict(
    policy='CosineAnnealing',
    min_lr=1e-5,
)

# 日志配置
log_config = dict(
    interval=1,    
    hooks=[
        dict(type='TextLoggerHook'),
    ])

# 模型配置
model = dict(
    type='TTFNet',
    backbone=dict(
        type='ResNet',
        depth=50, 
        in_channels=3, 
        out_indices=[3,2,1]),      
    neck=dict(type="FPN", in_channels=[512, 1024, 2048], out_channels=32, num_outs=3),
    bbox_head=dict(
        type='FcosHeadML',
        in_channel=32,
        feat_channel=32,
        num_classes=80,
        down_stride=[8,16,32],
        score_thresh=0.1,
        train_cfg=None,
        test_cfg=dict(topk=100, local_maximum_kernel=3, nms=0.3, max_per_img=10),
        loss_ch=dict(type='GaussianFocalLoss', loss_weight=1.0)
    ),  
)

# checkpoint配置
checkpoint_config = dict(interval=1, out_dir='./output/')       

# 数据配置
data=dict(
    train=dict(
        type='COCO2017',
        train_or_test='train',
        dir='./coco_dataset',
        ext_params={'task_type': 'OBJECT-DETECTION'},
        pipeline=[
            dict(type="Rotation", degree=15),
            dict(type='ResizeByShort', short_size=800, max_size=1333),
            dict(type='ColorDistort', hue=[-5,5,0.3], saturation=[0.8,1.2,0.3], contrast=[0.8,1.2,0.3], brightness=[0.8,1.2,0.3]),
            dict(type='RandomFlipImage', swap_labels=[]),
            dict(type='INormalize', mean=[128.0,128.0,128.0], std=[128.0,128.0,128.0],to_rgb=False, keys=['image']),
            dict(type='Permute', to_bgr=False, channel_first=True)
        ],
        inputs_def=dict(
            fields = ["image", 'bboxes', 'labels', 'image_meta']
        )
    ),
    train_dataloader=dict(
        samples_per_gpu=8, 
        workers_per_gpu=2,
        drop_last=True,
        shuffle=True,
        ignore_stack=['image', 'bboxes', 'labels', 'image_meta']
    ),
    val=dict(
        type='COCO2017',
        train_or_test='val',
        ext_params={'task_type': 'OBJECT-DETECTION'},
        dir='./coco_dataset',
        pipeline=[
            dict(type='ResizeByShort', short_size=800, max_size=1333),
            dict(type='INormalize', mean=[128.0,128.0,128.0], std=[128.0,128.0,128.0],to_rgb=False, keys=['image']),
            dict(type='Permute', to_bgr=False, channel_first=True)
        ],
        inputs_def=dict(
            fields= ["image", 'bboxes', 'labels', 'image_meta']
        )
    ),
    val_dataloader=dict(
        samples_per_gpu=8,
        workers_per_gpu=2,
        drop_last=False,
        shuffle=False,
        ignore_stack=['image', 'bboxes', 'labels', 'image_meta']
    ),
    test=dict(
        type='COCO2017',
        train_or_test='val',
        ext_params={'task_type': 'OBJECT-DETECTION'},
        dir='./coco_dataset',
        pipeline=[
            dict(type='ResizeByShort', short_size=800, max_size=1333),
            dict(type='INormalize', mean=[128.0,128.0,128.0], std=[128.0,128.0,128.0],to_rgb=False, keys=['image']),
            dict(type='Permute', to_bgr=False, channel_first=True)
        ],
        inputs_def=dict(
            fields= ["image", 'bboxes', 'labels', 'image_meta']
        )
    ),
    test_dataloader=dict(
        samples_per_gpu=10,
        workers_per_gpu=1,
        drop_last=False,
        shuffle=False,
        ignore_stack=['image','bboxes', 'labels', 'image_meta']
    ),    
)

# 评估方案配置
evaluation=dict(
    out_dir='./output/', 
    interval=1, 
    metric=dict(
        type='COCOCompatibleEval', 
        categories=[{'name': f'{label}', 'id': label} for label in range(80)],
        without_background=False
    ), 
    save_best='AP@[ IoU=0.50 | area= all | maxDets=100 ]',
    rule='greater'
)

# 导出配置
export=dict(
    input_shape_list = [[1,3,800,800]],
    input_name_list=["image"],
    output_name_list=["heatmap", "offset"]
)

max_epochs = 60