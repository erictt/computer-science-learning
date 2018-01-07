package common;

import java.io.File;
import java.io.FileNotFoundException;

public class StdIn {

  private static String dataPath = System.getProperty("user.dir")+"/algs4-data/";

  /**
   *
   * @param filename data file name, include extension
   * @return File object
   * @throws FileNotFoundException
   */
  public static File getDataFile(String filename) throws FileNotFoundException {
    File file = new File(dataPath + filename);
    if(!file.exists()) {
      throw new FileNotFoundException("File: " + filename + " doesn't exist.");
    }
    return file;
  }
}
