JOpenSurf: Java implementation of opensurf
==========================================

This is more or less a line for line port of the opensurf project released under the 3 clause BSD license. The original project is available at: http://code.google.com/p/opensurf1/
This project is up to date through revision 86 on the trunk branch of opensurf.


Ant Build File
---------------
This is a pretty small set of code, folks were having trouble getting it to work correctly (to be fair I forgot a couple of files ;)) so 
I included an ant buildfile. It's really only got three commands:

ant compile - This will compile the files

ant example - This will run an example which will show and compare the interest points for two images of the White House

ant clean - Cleans out the build directory files

Changes in sangupta/jopensurf fork
==================================

* The project has been Mavenized and refactored to follow Maven source structure
* The Apache Commons-Math library has been upgraded to version 3.2
* The **serialVersionUID** has been changed to generated ones
* A resource leak has been resolved
* Removed dependency on com.stromberglabs.commons JAR - the needed interface has been included in this codebase itself.

Maven
-----
The latest production release can be found at:
```xml
<dependency>
    <groupId>com.sangupta</groupId>
    <artifactId>jopensurf</artifactId>
    <version>1.0.0</version>
</dependency>
```

This is a Mavenized version of the original project.

License
-------
The project follows the original 3 clause BSD license.
