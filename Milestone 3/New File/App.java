package medical.com.medicalApplication; // Import Medical Application Class

import java.util.Arrays; 	// Import Java Arrays utility
import java.util.List;  	// Import Java List utility 
import java.util.Scanner;	// Import Java Scanner utility

import medical.com.medicalApplication.model.Employee; 					// Import Employee model from Medical Application Class
import medical.com.medicalApplication.prompts.MedicalRecordPrompt;		// Import Medical Record Prompt from Medical Application Class
import medical.com.medicalApplication.services.DoctorService;			// Import Doctor Service from Medical Application Class
import medical.com.medicalApplication.services.MedicalRecordService;	// Import Medical RecordService from Medical Application Class
import medical.com.medicalApplication.util.MenuUtil;					// Import Menu Utility from Medical Application Class
import medical.com.medicalApplication.util.Pair;						// Import Pair Utility from Medical Application Class

// Add duplicate doctors
// Adding medical records
// Find Allergies per patient

public class App {
	
	private static List<String> mainMenu = Arrays.asList("", "Main Menu", "Please select from the following options",
			"1 Print Patient List", "2 Print Doctor List", "3 Add a Doctor", "4 Add a Patient", "5 Medical Records",
			"6 Search for Allergies", "0 to Exit");

	public static void main(String[] args) {
		
		// Created for testing purposes password is "Open"
		Employee employee = new Employee("Mike", "1111");
		
		// Read console input
		Scanner scanner = new Scanner(System.in);
		scanner.useDelimiter(System.getProperty("line.separator"));

		
		// Declares and assigns variables used by login logic
		int passwordAttepts = 3;
		String password = null;
		boolean loginSuccess = false;
		
		// Login logic, allows three attempts
		while (passwordAttepts > 0 && !loginSuccess) {
			System.out.println("Login Enter Password");
			password = scanner.next();
			loginSuccess = employee.getPassword().equals(password);
			passwordAttepts--;
		}

		
		// If loop checks for login status before allowing access to menu
		if (loginSuccess) {
			MedicalRecordPrompt medicalRecordPrompt = new MedicalRecordPrompt();
			int input = -1;
			System.out.println("Welcome to Mercy Hospitol System");
			
			// While loop populates menu and calls functions based on user selections 
			while (input != 0) {
				mainMenu.stream().forEach(System.out::println);
				input = scanner.nextInt();

				// Switch cases that represent menu options and their underlying function. 
				switch (input) {
				case 1:
					MedicalRescordService.getReference().getAllPatients().forEach(System.out::println);
					break;
				case 2:
					DoctorService.getReference().getAllDoctors().forEach(System.out::println);
					break;
				case 3:
					addPerson(true, scanner);
					break;
				case 4:
					addPerson(false, scanner);
					break;
				case 5:
					medicalRecordPrompt.mainPrompt(scanner);
					break;
				case 6:
					medicalRecordPrompt.findAllPatientsWithAllergy(scanner).forEach(System.out::println);
					break;
				case 0:
					System.out.println("Good bye!");
					break;
				default:
					break;
				}
			}
			scanner.close();
		}else{
			System.out.println("Invalid Password after 3 tries");
		}
	}

	// Logic that allows addition of doctors or patients
	private static void addPerson(boolean addDoctor, Scanner scanner) {
		int input = -1;
		String person = addDoctor ? "Doctor" : "Patient";

		// While loop with nexted if/else logic that adds doctors or patients based on user input. 
		while (input != 0) {
			Pair response = MenuUtil.createTwoItemMenu(scanner, "Enter Name:", "Enter ID:");
			boolean personAdded = false;

			if (addDoctor) {
				personAdded = DoctorService.getReference().addDoctor(response.getOne(), response.getTwo());
			} else {
				personAdded = MedicalRescordService.getReference().addPatient(response.getOne(), response.getTwo());
			}

			if (personAdded) {
				System.out.println(person + " " + response.getOne() + " was succesfully added\n");
			} else {
				System.out.println(person + " " + response.getOne() + " Could not be added\n");
			}
			System.out.println(
					"Would you like to add another " + person + "?\n 1 for Yes\n 0 To return to the Main Menu");
			input = scanner.nextInt();
		}
	}

}
