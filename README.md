[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

* The dataset will be uploaded very soon

# Critical Infrastructures - CI dataset

The automatic critical infrastructures detection system analyses a satellite image through a detector and returns the infrastructures that appear in the image. This system is achieved through Deep Learning (DL) techniques based on convolutional neural networks (CNN) that can be trained to detect this type of objects.

The critical infrastructure detection task depends on the input image since the satellite images are given according to the zoom level. This zoom level indicates the actual size in meters occupied by a pixel of the image. As each infrastructure can be detected in a range of zoom levels, it is possible to obtain specialized detectors in ranges of zoom levels. The strategy to perform the detections can be to apply all detectors to an image, or to apply the DetDSCI methodology to classify the input image according to its zoom level to select its specialized detector. However, any DL model requires to learn a quality image dataset and annotation according to the detection task.

Critical Infrastructures - CI dataset provides quality image datasets built for training DL models in the framework of developing an automatic critical infrastructure detection system. Each dataset for the image object detection task is described below and can be downloaded. The public datasets are organized depending on the objects included in the dataset and the range of zoom levels.

You can read more information about this dataset in [Critical Infrastructures - CI dataset](https://dasci.es/transferencia/open-data/ci-dataset/)

### Contact

[***Fransco Pérez Hernandez***](https://www.linkedin.com/in/franciscoperezhernandez/)
- Personal email: fperezhernandez92@gmail.com
- Institutional email: fperezhernandez@ugr.es

[***José Rodríguez Ortega***](https://www.linkedin.com/in/jose-rodr%C3%ADguez-ortega)
- Personal email: jrodriguezortega98@gmail.com
- Institutional email: jrodriguez98@correo.ugr.es

## Reference
```
Pérez-Hernández, F., Rodríguez-Ortega, J., Benhammou, Y., Herrera, F., & Tabik, S. (2021). CI-dataset and DetDSCI methodology for detecting too small and too large critical infrastructures in satellite images: Airports and electrical substations as case study. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 14, 12149-12162.
```


### License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg