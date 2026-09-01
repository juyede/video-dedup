"""
视频去重系统使用示例

展示了3种不同的使用方式：
1. 找重复视频对
2. 聚类相似视频
3. 比较单个视频对
"""

from video_dedup import VideoDeduplicator, VideoDeduplicator
import os


def example1_find_duplicates():
    """示例1: 找重复视频对"""
    print("\n" + "=" * 80)
    print("示例1: 找重复视频对 (Find Duplicate Videos)")
    print("=" * 80)
    
    # 视频列表
    videos = [
        "test_videos/video_1_original.mp4",
        "test_videos/video_1_duplicate.mp4",
        "test_videos/video_2_unique.mp4",
        "test_videos/video_4_text.mp4",
        "test_videos/video_4_text_copy.mp4",
    ]
    
    # 过滤存在的视频
    videos = [v for v in videos if os.path.exists(v)]
    
    if not videos:
        print("❌ No test videos found. Run: python test_videos.py")
        return
    
    # 初始化去重系统
    dedup = VideoDeduplicator(
        clip_threshold=0.90,
        flow_threshold=0.80,
        combined_threshold=0.85,
        use_clip=True
    )
    
    # 找重复
    duplicates = dedup.find_duplicates(videos)
    
    # 输出结果
    print(f"\n📊 结果 (Results):")
    print(f"  找到 {len(duplicates)} 对重复视频\n")
    
    for video1, video2, similarity in duplicates:
        print(f"  ✓ {os.path.basename(video1)}")
        print(f"    ↔ (相似度: {similarity:.4f})")
        print(f"    {os.path.basename(video2)}")
        print()


def example2_cluster_videos():
    """示例2: 聚类相似视频"""
    print("\n" + "=" * 80)
    print("示例2: 聚类相似视频 (Cluster Similar Videos)")
    print("=" * 80)
    
    # 视频列表
    videos = [
        "test_videos/video_1_original.mp4",
        "test_videos/video_1_duplicate.mp4",
        "test_videos/video_2_unique.mp4",
        "test_videos/video_3_random.mp4",
        "test_videos/video_4_text.mp4",
        "test_videos/video_4_text_copy.mp4",
    ]
    
    # 过滤存在的视频
    videos = [v for v in videos if os.path.exists(v)]
    
    if not videos:
        print("❌ No test videos found. Run: python test_videos.py")
        return
    
    # 初始化去重系统
    dedup = VideoDeduplicator(
        combined_threshold=0.85,
        use_clip=True
    )
    
    # 聚类
    clusters = dedup.cluster_videos(videos)
    
    # 输出结果
    print(f"\n📊 结果 (Results):")
    print(f"  创建了 {len(clusters)} 个集群\n")
    
    for cluster_id, cluster_videos in sorted(clusters.items()):
        print(f"  📁 集群 {cluster_id}:")
        for video in cluster_videos:
            print(f"     - {os.path.basename(video)}")
        print()


def example3_compare_two_videos():
    """示例3: 比较两个视频"""
    print("\n" + "=" * 80)
    print("示例3: 比较两个视频 (Compare Two Videos)")
    print("=" * 80)
    
    # 两个视频
    video1 = "test_videos/video_1_original.mp4"
    video2 = "test_videos/video_1_duplicate.mp4"
    
    if not os.path.exists(video1) or not os.path.exists(video2):
        print("❌ Test videos not found. Run: python test_videos.py")
        return
    
    # 初始化去重系统
    dedup = VideoDeduplicator(use_clip=True)
    
    # 比较
    result = dedup.compare_videos(video1, video2)
    
    # 输出结果
    print(f"\n📊 比较结果 (Comparison Result):")
    print(f"  视频1: {os.path.basename(result.video1)}")
    print(f"  视频2: {os.path.basename(result.video2)}")
    print()
    print(f"  指标 (Metrics):")
    print(f"    - CLIP 相似度: {result.clip_similarity:.4f}")
    print(f"    - 光学流相似度: {result.optical_flow_similarity:.4f}")
    print(f"    - 综合相似度: {result.combined_similarity:.4f}")
    print()
    print(f"  判断 (Decision):")
    if result.is_duplicate:
        print(f"    ✓ 这是重复视频 (Duplicate)")
    else:
        print(f"    ✗ 这不是重复视频 (Not Duplicate)")


def example4_advanced_parameters():
    """示例4: 高级参数调整"""
    print("\n" + "=" * 80)
    print("示例4: 高级参数调整 (Advanced Parameters)")
    print("=" * 80)
    
    videos = [
        "test_videos/video_1_original.mp4",
        "test_videos/video_1_duplicate.mp4",
        "test_videos/video_2_unique.mp4",
    ]
    
    videos = [v for v in videos if os.path.exists(v)]
    
    if not videos:
        print("❌ No test videos found. Run: python test_videos.py")
        return
    
    # 示例 1: 严格去重（只找完全重复）
    print("\n🔒 严格去重 (Strict Deduplication)")
    print("   阈值: 0.95")
    dedup_strict = VideoDeduplicator(combined_threshold=0.95, use_clip=True)
    duplicates = dedup_strict.find_duplicates(videos)
    print(f"   找到: {len(duplicates)} 对\n")
    
    # 示例 2: 宽松去重（找相似视频）
    print("🔓 宽松去重 (Loose Deduplication)")
    print("   阈值: 0.75")
    dedup_loose = VideoDeduplicator(combined_threshold=0.75, use_clip=True)
    duplicates = dedup_loose.find_duplicates(videos)
    print(f"   找到: {len(duplicates)} 对\n")
    
    # 示例 3: 仅使用光学流
    print("🚫 仅光学流 (Optical Flow Only)")
    print("   禁用CLIP模型")
    dedup_flow = VideoDeduplicator(use_clip=False)
    duplicates = dedup_flow.find_duplicates(videos)
    print(f"   找到: {len(duplicates)} 对\n")


def example5_batch_processing():
    """示例5: 批量处理"""
    print("\n" + "=" * 80)
    print("示例5: 批量处理 (Batch Processing)")
    print("=" * 80)
    
    # 查找所有测试视频
    video_dir = "test_videos"
    if not os.path.exists(video_dir):
        print("❌ test_videos directory not found. Run: python test_videos.py")
        return
    
    videos = [
        os.path.join(video_dir, f)
        for f in os.listdir(video_dir)
        if f.endswith(".mp4")
    ]
    
    if not videos:
        print("❌ No videos found in test_videos/")
        return
    
    print(f"\n📹 找到 {len(videos)} 个视频:")
    for v in videos:
        print(f"   - {os.path.basename(v)}")
    
    # 初始化
    dedup = VideoDeduplicator(use_clip=True)
    
    # 批量处理
    print(f"\n⚙️ 处理中...")
    duplicates = dedup.find_duplicates(videos)
    
    print(f"\n📊 结果:")
    print(f"   找到 {len(duplicates)} 对重复视频")
    
    # 生成报告
    print(f"\n📝 生成报告...")
    dedup.generate_report(videos, output_dir="results")
    print(f"   ✓ 报告已保存到 results/dedup_report.txt")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🎬 视频去重系统 - 使用示例 (Video Deduplication Examples)")
    print("=" * 80)
    
    try:
        # 运行所有示例
        example1_find_duplicates()
        example2_cluster_videos()
        example3_compare_two_videos()
        example4_advanced_parameters()
        example5_batch_processing()
        
        print("\n" + "=" * 80)
        print("✓ 所有示例完成 (All examples completed)")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n❌ 中断 (Interrupted)")
    except Exception as e:
        print(f"\n\n❌ 错误 (Error): {e}")
        import traceback
        traceback.print_exc()
