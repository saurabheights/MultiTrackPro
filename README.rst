=============
MultiTrackPro
=============


.. image:: https://img.shields.io/pypi/v/multitrackpro.svg
        :target: https://pypi.python.org/pypi/multitrackpro

.. image:: https://readthedocs.org/projects/multitrackpro/badge/?version=latest
        :target: https://multitrackpro.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A multi-camera multi-object tracking library with its own labelling tool to annotate datasets.


* Free software: GNU General Public License v3
* Documentation: https://readthedocs.org/projects/multitrackpro/.


Features
--------

* QT based media player that can play four videos at the same time.

.. code-block:: shell

   auto-annotate-pro

Pending Tasks
-------------

* Integrate object detection and tracker.
    * Store annotations of each frame in mem.
    * Add display of bounding boxes as drawables.
    * Save/Load Annotations.
    * Save dataset-specific configuration.
* Add object detection correction
* Add tracking correction
* Add mouse event capture to rearrange videos.
* Add track integration between two frames.
* Add play pause icons to UI.
* Set play pause next fram, prev frame etc buttons to disabled stage when no video.
* Add speed change option for playback.
* Make frame number text label and slider work.
* Integrate github action/circleci
* Implement play of N number of video files (N != 4).

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
