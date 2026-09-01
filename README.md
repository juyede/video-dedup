# 视频去重系统 (Video Deduplication System)

一个完整的视频去重解决方案，支持光学流分析、CLIP多模态向量和时间分析，适用于内容审核研究。

## 🌟 特性

- **多种去重方法**：
  - 🔄 光学流（Optical Flow）运动分析
  - 🎨 CLIP多模态向量相似度
  - 📊 综合相似度计算
  - 🎯 层次聚类

- **灵活的运行模式**：
  - `duplicates`: 找到所有重复视频对
  - `cluster`: 将相似视频分组
  - `compare`: 比较两个视频

- **详细的分析报告**
- **支持GPU加速**

## 📋 环境要求

```bash
# Python 3.8+
# 依赖项
pip install -r requirements.txt

# 还需要 FFmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# 从 https://ffmpeg.org/download.html 下载
```

## 🚀 快速开始

### 1. 生成测试视频

```bash
python test_videos.py
```

这会创建5个测试视频（包括重复和不同的视频）。

### 2. 运行去重

```bash
# 方式 1: 找重复视频
python video_dedup.py \
  --videos test_videos/video_*.mp4 \
  --mode duplicates \
  --output results/

# 方式 2: 聚类相似视频
python video_dedup.py \
  --videos test_videos/video_*.mp4 \
  --mode cluster \
  --output results/

# 方式 3: 比较两个视频
python video_dedup.py \
  --videos test_videos/video_1_original.mp4 test_videos/video_1_duplicate.mp4 \
  --mode compare
```

### 3. 查看结果

```bash
cat results/dedup_report.txt
```

## 📖 详细使用说明

### 命令行参数

```
--videos          视频文件路径 (必需)
--output          输出目录 (默认: results)
--clip-threshold  CLIP相似度阈值 (默认: 0.90)
--flow-threshold  光学流相似度阈值 (默认: 0.80)
--combined-threshold  综合相似度阈值 (默认: 0.85)
--no-clip         禁用CLIP模型（仅使用光学流）
--mode            运行模式: duplicates/cluster/compare (默认: duplicates)
```

### Python API 使用

```python
from video_dedup import VideoDeduplicator

# 初始化
dedup = VideoDeduplicator(
    clip_threshold=0.90,
    flow_threshold=0.80,
    combined_threshold=0.85,
    use_clip=True  # 使用CLIP
)

# 方式 1: 找重复
video_paths = ["video1.mp4", "video2.mp4", "video3.mp4"]
duplicates = dedup.find_duplicates(video_paths)

for video1, video2, similarity in duplicates:
    print(f"重复: {video1} ↔ {video2} (相似度: {similarity:.3f})")

# 方式 2: 聚类
clusters = dedup.cluster_videos(video_paths)

for cluster_id, videos in clusters.items():
    print(f"集群 {cluster_id}: {videos}")

# 方式 3: 比较两个视频
result = dedup.compare_videos("video1.mp4", "video2.mp4")

print(f"CLIP 相似度: {result.clip_similarity:.4f}")
print(f"光学流相似度: {result.optical_flow_similarity:.4f}")
print(f"综合相似度: {result.combined_similarity:.4f}")
print(f"是重复: {result.is_duplicate}")

# 方式 4: 生成完整报告
dedup.generate_report(video_paths, output_dir="results/")
```

## 🔍 技术细节

### 光学流分析

使用 Farneback 方法计算密集光学流：
- 检测帧间的运动
- 计算运动强度序列
- 使用 DTW 距离比较运动模式

```python
# 示例
analyzer = OpticalFlowAnalyzer(method="farneback")
motion_profile = analyzer.extract_motion_features("video.mp4")
# motion_profile shape: (T,) - 运动强度序列
```

### CLIP 多模态向量

使用 CLIP 模型提取视频的语义特征：
- 均匀采样视频帧
- 每帧提取图像特征
- 平均池化得到视频向量

```python
# 示例
clip_analyzer = CLIPVideoAnalyzer()
embedding = clip_analyzer.extract_video_embedding("video.mp4")
# embedding shape: (512,) - CLIP向量
```

### 相似度计算

#### CLIP 相似度
```
similarity = dot_product(emb1_norm, emb2_norm)
```
- 范围: [0, 1]
- 1 = 完全相同, 0 = 完全不同

#### 光学流相似度
```
similarity = 1 / (1 + DTW_distance)
```
- 基于动态时间规整
- 比较运动模式

#### 综合相似度
```
combined = 0.6 * clip_sim + 0.4 * flow_sim
```
- 加权平均
- 平衡视觉内容和运动特征

## 📊 输出示例

### 重复视频对
```
重复视频对 (Duplicate Pairs)
================================================================================
  video_1_original.mp4
  ↔
  video_1_duplicate.mp4
  相似度: 0.9523
================================================================================
```

### 视频聚类
```
视频聚类 (Video Clusters)

  集群 0:
    - video_1_original.mp4
    - video_1_duplicate.mp4

  集群 1:
    - video_2_unique.mp4

  集群 2:
    - video_4_text.mp4
    - video_4_text_copy.mp4
```

## ⚙️ 参数调整

根据你的需求调整相似度阈值：

- **严格去重** (寻找完全重复):
  ```bash
  --combined-threshold 0.95
  ```

- **宽松去重** (寻找相似视频):
  ```bash
  --combined-threshold 0.75
  ```

- **仅使用光学流** (不使用CLIP):
  ```bash
  --no-clip
  ```

## 🎯 应用场景

1. **短视频平台去重** - 快手、抖音等
2. **内容审核** - 检测相似有害内容
3. **版权检测** - 发现剽窃或再上传的视频
4. **数据去重** - 机器学习训练集清理
5. **视频搜索** - 查找相似视频

## 🔬 学术应用

这个系统可用于研究：
- 视频相似度指标
- 多模态特征融合
- 对抗样本（修改视频使其绕过去重）
- 审核系统鲁棒性

## 📈 性能指标

| 操作 | 时间（秒） | 内存（GB） |
|------|----------|----------|
| 提取光学流（3分钟视频） | ~30 | 0.5 |
| 提取CLIP向量（3分钟视频） | ~10 | 2.0 |
| 比较两个视频 | ~0.001 | 0.1 |
| 聚类100个视频 | ~300 | 1.0 |

## 🛠️ 故障排除

### 问题: CLIP 模型加载失败
```
❌ Error: Could not load CLIP model
```

**解决**:
```bash
pip install --upgrade transformers torch
# 或使用 --no-clip 禁用CLIP
python video_dedup.py --videos ... --no-clip
```

### 问题: 内存不足
```
❌ RuntimeError: CUDA out of memory
```

**解决**:
- 减少采样帧数
- 使用 CPU 而不是 GPU
- 处理更小的视频

### 问题: FFmpeg 未找到
```
❌ FileNotFoundError: ffmpeg not found
```

**解决**: 安装 FFmpeg（见环境要求）

## 📝 许可证

MIT License

## 📧 联系方式

有问题或建议？提交 Issue 或 Pull Request。

## 🙏 致谢

- OpenAI CLIP 模型
- OpenCV 图像处理库
- PyTorch 深度学习框架

---

**提示**: 这是一个学术研究项目。在生产环境中使用前，请确保遵守相关法律法规和隐私政策。
