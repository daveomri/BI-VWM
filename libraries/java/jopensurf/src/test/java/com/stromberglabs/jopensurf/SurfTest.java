package com.stromberglabs.jopensurf;

import static org.junit.Assert.assertTrue;

import java.io.File;

import javax.imageio.ImageIO;

import org.junit.Ignore;
import org.junit.Test;


public class SurfTest {
	
	/**
	 * This is a simple function that just tests that the high level output
	 * from lenna.png . I am using this to test refactoring so that I can insure
	 * that the output of the algorithm didn't change 
	 * 
	 * @throws Exception
	 */
	@Test
	@Ignore("fails due to class serialization errors")
	public void testSURFOutput() throws Exception {
		// get classpath
		String originalFile = this.getClass().getClassLoader().getResource("example/lenna_surf_test.bin").getFile();
		if(originalFile.startsWith("/")) {
			originalFile = originalFile.substring(1);
		}
		
		String currentFile = this.getClass().getClassLoader().getResource("example/lenna.png").getFile();
		if(currentFile.startsWith("/")) {
			currentFile = currentFile.substring(1);
		}
		
		Surf original = Surf.readFromFile(originalFile);
		Surf current = new Surf(ImageIO.read(new File(currentFile)));
		
		//Surf.saveToFile(current,"H:\\workspace\\javaopensurf\\example\\lenna_surf_test.bin");
		assertTrue(original.isEquivalentTo(current));
	}
	
}
