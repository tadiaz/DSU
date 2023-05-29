import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Scanner;

public class stegan {
   public static void main(String args[]) throws Exception {
	System.out.print("Enter image filename: ");
	Scanner kb = new Scanner(System.in);
	String filename = kb.nextLine();
	System.out.print("Enter a text filename: ");
	String text_filename = kb.nextLine();
	
	hide(filename, text_filename);
   }

   public static void hide(String filename, String text_filename) throws Exception{
	String filePath = text_filename;

	byte[] bytes1 = Files.readAllBytes(Paths.get(filePath));

      BufferedImage bImage = ImageIO.read(new File(filename));
      ByteArrayOutputStream bos = new ByteArrayOutputStream();
      ImageIO.write(bImage, "jpg", bos );
      byte [] data = bos.toByteArray();
	byte[] data2 = new byte[data.length];

	String s1="";
	String s2="";
	for(int i = 0; i<data.length; ++i)
	{
		s1 += String.format("%8s", Integer.toBinaryString(data[i] & 0xFF)).replace(' ', '0');
	}
	for(int i = 0; i<bytes1.length; ++i)
	{
		s2 += String.format("%8s", Integer.toBinaryString(bytes1[i] & 0xFF)).replace(' ', '0');
	}
	s2="00110011001100110011001100110011"+s2;
	String s3= s1.substring(0,(s1.length()-64))+s2+s1.substring((s1.length()-64), s1.length());

	int l = 0;
	data2 = new byte[s3.length()];
	for(int i = 0; i < s3.length(); i+=8)
	{
		byte b;
		if(i+8<s3.length())
			b = getDecimal(Integer.parseInt(s3.substring(i,i+8)));
		else
			b = getDecimal(Integer.parseInt(s3.substring(i,s3.length())));
		data2[l]=b;
		++l;
	}

      ByteArrayInputStream bis = new ByteArrayInputStream(data2);
      BufferedImage bImage2 = ImageIO.read(bis);
      ImageIO.write(bImage2, "jpg", new File("output.jpg") );
	System.out.println(s3);
      System.out.println("image created");
   }

   public static byte getDecimal(int binary){  
      byte decimal = 0;  
      byte n = 0;  
      while(true){  
         if(binary == 0){  
           break;  
         } else {  
           byte temp = (byte)(binary%10);  
           decimal += temp*Math.pow(2, n);  
           binary = binary/10;  
           n++;  
         }  
      }  
      return decimal;  
   }  
}