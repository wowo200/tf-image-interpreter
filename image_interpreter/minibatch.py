import numpy as np
from scipy import ndimage


class BatchGenerator(object):
  def __init__(self, roidb):
    self._roidb = roidb
    self._total = len(roidb.all_meta)
    self._cur = 0
    self._perm = np.random.permutation(self._total)
    self._image_scale_size = 600

  def next_batch(self):
    if self._cur >= self._total:
      self._shuffle()

    ind = self._perm[self._cur]
    self._cur += 1

    return self._generate_batch(self._roidb.all_meta[ind])

  def _shuffle(self):
    self._perm = np.random.permutation(self._total)
    self._cur = 0

  def _generate_batch(self, meta):
    image = ndimage.imread(meta.image_path)
    height, width, _ = meta.shape
    if height > width:
      scale = self._image_scale_size / width
    else:
      scale = self._image_scale_size / height

    # TODO: the dimensions in caffe is (batch elem, channel, height, width)
    resized_image = ndimage.zoom(image, (scale, scale, 1))
    bboxes = np.empty((len(meta.objects), 5))
    for i, obj in enumerate(meta.objects):
      bboxes[i][:4] = obj['bbox']
      bboxes[i][4] = obj['class_index']

    return np.expand_dims(resized_image, 0), scale, bboxes
