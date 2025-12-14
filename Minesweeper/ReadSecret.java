/**
 * In this class's main method you will read a file that has an encoded message and 
 * print out to the console the decoded message
 * 
 * You will need to READ the examples from reading from M7 - Read and Try: File I/O
 * "Introduction To File Input And Ouput Gaddis"
 * 
 * Before coding in Java, let's brainstorm our high level process:
 * 1.) File location
 * 2.) Open
 * 3.) Read
 * 4.) Decode
 * 5.) Print
 */
import java.io.File;
import java.io.FileNotFoundException;
import java.util.InputMismatchException;
import java.util.Scanner;

public class ReadSecret
{
		public static void main(String[] args) {
			// String inputFilePath = "./msg/SecretMessage1.txt";

			// For VSC only(since my Java runner choose my project root as working directory, not the file's directory)
			// inputFilePath = "./SecretFile/M7SecretFiles - StudentTemplates/msg/SecretMessage1.txt";
			
			// File secretFile = new File(inputFilePath);
			// The code above is for a single file to be chosen, and user have to know the file name beforehand


			// The code below is for user to choose from a list of files from "msg" folder
			// Only works on BlueJ(directory = file's directory)
			File msgFolder = new File("./msg");
			File[] listOfFiles = msgFolder.listFiles();
			System.out.println("Files available:");
			int counter = 1;
			for (File file : listOfFiles) {
				if (file.isFile()) {
					System.out.println(counter + ") " + file.getName());
				}
				counter++;
			}
			System.out.print("Chosen file: ");
			Scanner scanner = new Scanner(System.in);
			int fileChoice = 0;
			try {
				fileChoice = scanner.nextInt();
				File chosenFile = listOfFiles[fileChoice - 1];
			} catch (Exception e) {
				// Normally, I would put a InputMismatchException here, but to be safe I just put a general Exception since I want to catch all invalid inputs including out of bound indexes(like 4 when there are only 3 files) and non-integer inputs
				System.out.println("Invalid input. Please enter a number corresponding to the file.");
			}
			scanner.close();
			// File secretFile = new File(FileChooser.pickAFile());

			try (Scanner reader = new Scanner(listOfFiles[fileChoice - 1])) {
				int length = (int) reader.nextInt();
				int[] encodedMessage = new int[length];
				for (int i = 0; i < length; i++) {
					encodedMessage[i] = reader.nextInt();
				}

				reader.close();
				
				String decoded = SecretCode.decode(encodedMessage);
				System.out.println("The decoded message is: " + decoded);
			} catch (FileNotFoundException error) {
				System.out.println("An error occurred. Can not find specified file.");
				error.printStackTrace();
			}
		}
}