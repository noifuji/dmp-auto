package resizeimage;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Locale;
import javax.imageio.IIOImage;
import javax.imageio.ImageIO;
import javax.imageio.ImageWriteParam;
import javax.imageio.ImageWriter;
import javax.imageio.plugins.jpeg.JPEGImageWriteParam;
import javax.imageio.stream.ImageOutputStream;

public class ResizeImage {

  public String resize(String filename, double n) {
    int resizeW;
    int resizeH;
  	String newFilename = "";
  	
    try{
      File fileBeforeResize = new File(filename);
      String fileNameBeforeResize = fileBeforeResize.getName();
      String fileNameBeforeResizeWithoutExt = fileNameBeforeResize.substring(0, fileNameBeforeResize.lastIndexOf('.'));
	  String ext = fileNameBeforeResize.substring(fileNameBeforeResize.lastIndexOf(".") + 1);
      BufferedImage original = ImageIO.read(fileBeforeResize);

      resizeW = (int)(original.getWidth() * n);
      resizeH = (int)(original.getHeight() * n);

      // 画像サイズ変更
      BufferedImage scaleImg = new BufferedImage(resizeW, resizeH, BufferedImage.TYPE_3BYTE_BGR);
      scaleImg.createGraphics().drawImage(
        original.getScaledInstance(resizeW, resizeH, Image.SCALE_AREA_AVERAGING),
        0, 0, resizeW, resizeH, null);

      newFilename = fileBeforeResize.getParent() + File.separator + fileNameBeforeResizeWithoutExt + "small." + ext;
      try (ImageOutputStream imageStream = ImageIO.createImageOutputStream(new File(newFilename))) {
        JPEGImageWriteParam param = new JPEGImageWriteParam(Locale.getDefault());
        param.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
        param.setCompressionQuality(1f);
        ImageWriter writer = ImageIO.getImageWritersByFormatName("png").next();
        writer.setOutput(imageStream);
        writer.write(null, new IIOImage(scaleImg, null, null), param);
        imageStream.flush();
        writer.dispose();
      }
    }catch(Exception e) {
      System.out.println(e);
    }
  	
  	return newFilename;
  }
}