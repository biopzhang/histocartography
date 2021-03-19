"""Unit test for preprocessing.stain_normalizers"""
import unittest
import numpy as np
import cv2 
import torch 
import yaml
import dgl
import os
from PIL import Image
import shutil

from histocartography import PipelineRunner
from histocartography.preprocessing import MacenkoStainNormalizer, VahadaneStainNormalizer


class StainNormalizationTestCase(unittest.TestCase):
    """StainNormalizationTestCase class."""

    @classmethod
    def setUpClass(self):
        self.current_path = os.path.dirname(__file__)
        self.data_path = os.path.join(self.current_path, '..', 'data')
        self.image_path = os.path.join(self.data_path, 'images')
        self.target_name = '16B0001851.png'
        self.image_name = '16B0006669.png'
        self.out_path = os.path.join(self.data_path, 'stain_normalization_test')
        if os.path.exists(self.out_path) and os.path.isdir(self.out_path):
            shutil.rmtree(self.out_path) 
        os.makedirs(self.out_path)

    def test_macenko_normalizer_no_ref(self):
        """
        Test Macenko Stain Normalization: without Reference.
        """

        image = np.array(Image.open(os.path.join(self.image_path, self.image_name)))

        stain_normalizer = MacenkoStainNormalizer(
            base_path=self.out_path,
        )
        stain_normalizer.precompute(self.image_path)
        image_norm = stain_normalizer.process(image)

        self.assertTrue(isinstance(image_norm, np.ndarray))  # output is numpy
        self.assertEqual(list(image.shape), list(image_norm.shape))  # image HxW = mask HxW

    def test_macenko_normalizer_ref(self):
        """
        Test Macenko Stain Normalization: with Reference.
        """

        image = np.array(Image.open(os.path.join(self.image_path, self.image_name)))

        stain_normalizer = MacenkoStainNormalizer(
            base_path=self.out_path,
            target=self.target_name.replace('.png', ''),
            target_path=os.path.join(self.image_path, self.target_name)
        )
        stain_normalizer.precompute(self.image_path)
        image_norm = stain_normalizer.process(image)

        self.assertTrue(isinstance(image_norm, np.ndarray))  # output is numpy
        self.assertEqual(list(image.shape), list(image_norm.shape))  # image HxW = mask HxW

    def test_vahadane_normalizer_no_ref(self):
        """
        Test Vahadane Stain Normalization: without Reference.
        """

        image = np.array(Image.open(os.path.join(self.image_path, self.image_name)))

        stain_normalizer = VahadaneStainNormalizer(
            base_path=self.out_path,
        )
        stain_normalizer.precompute(self.image_path)
        image_norm = stain_normalizer.process(image)

        self.assertTrue(isinstance(image_norm, np.ndarray))  # output is numpy
        self.assertEqual(list(image.shape), list(image_norm.shape))  # image HxW = mask HxW

    def test_vahadane_normalizer_ref(self):
        """
        Test Vahadane Stain Normalization: with Reference.
        """

        image = np.array(Image.open(os.path.join(self.image_path, self.image_name)))

        stain_normalizer = VahadaneStainNormalizer(
            base_path=self.out_path,
            target=self.target_name.replace('.png', ''),
            target_path=os.path.join(self.image_path, self.target_name)
        )
        stain_normalizer.precompute(self.image_path)
        image_norm = stain_normalizer.process(image)

        self.assertTrue(isinstance(image_norm, np.ndarray))  # output is numpy
        self.assertEqual(list(image.shape), list(image_norm.shape))  # image HxW = mask HxW

    def test_vahadane_invalid_precomputed_normalizer(self):
        """
        Test Vahadane invalid precomputed normalization.
        """
        stain_normalizer = VahadaneStainNormalizer(
            base_path=self.out_path,
            precomputed_normalizer='./temp.h5'
        )
        with self.assertRaises(FileNotFoundError):
            stain_normalizer.precompute(self.image_path)

    def tearDown(self):
        """Tear down the tests."""


if __name__ == "__main__":
    unittest.main()
