=============
MultiTrackPro
=============


.. image:: https://img.shields.io/pypi/v/multitrackpro.svg
        :target: https://pypi.python.org/pypi/multitrackpro

.. image:: https://readthedocs.org/projects/multitrackpro/badge/?version=latest
        :target: https://multitrackpro.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A multi-camera multi-object tracking software with its own labelling tool to annotate datasets.


* Free software: GNU General Public License v3
* Documentation: https://readthedocs.org/projects/multitrackpro/.


Features
--------

* QT based media player that can play four videos at the same time.

.. code-block:: shell

   auto-annotate-pro

Pending Tasks
-------------

* Implement play of N number of video files (N != 4, but N <=4). Limit to 4 videos maximum.
* Set play pause next frame, prev frame etc buttons to disabled stage when no video.
* Add play pause icons to UI using `Google Material`_.

* Integrate object detection.
    * ☑ - Store annotations of each frame in memory.
    * ☑ - Add display of bounding boxes.
    * Replace BoundingBox as drawables.
    * Add tracker.
    * Save/Load Annotations.
    * Save dataset-specific configuration.
* Add masking to the frames to discard object detection for certain areas.
* Add object detection correction
* Add tracking correction
* Add mouse event capture to rearrange videos.
* Add track integration between two frames.

* Add speed change option for playback.
* Make frame number text label and slider work.
* Integrate github action/circleci
* ToDo - See Live Preview of object detection and tracking. This will help user catch errors quickly, instead of running object detection completely.
* Use platformdirs_

.. _Google Material: https://fonts.google.com/icons?icon.category=Audio%26Video
.. _platformdirs: https://github.com/platformdirs/platformdirs

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
