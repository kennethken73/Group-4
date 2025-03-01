/*
* Name: Richard Vargason, 2001951923, Assignment #1
* Description: Reads in cereal.txt, a list of cereal and their attributes, and allows for sorting/printing out of that list 
* Input: cereal.txt
* Output: User created file
*/


/*tab = \t; 
argc = argument count
argv = the list of args
g++ -std=c++11 main.cpp
./a.exe
*/

#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
using namespace std;

//declaring cereal struct with all cereal attributes
struct cereal {
    string name;
    char mfr, type;
    int calories, protein, fat, sodium, sugars, potass, vitamins, shelf;
    float fiber, carbo, weight, cups, rating;
};

const int maxSize = 100;
string words;

// Function to read the file
bool readFile(string fName , cereal cArr[], int &cSize);
// Function to print a cereal
void printCereal(const cereal &c, ostream &out);
// Function to print all cereals
void printCerealArr(const cereal cArr[], const int &cSize , ostream &out);
// Function to extract a numeric field from cereal
float getNumber(string fieldName , const cereal &c);
// Function to extract char field from cereal
char getChar(string fieldName , const cereal &c);
// Function to extract the name of cereal
string getName(const cereal &c);
// Function to print the menu and get input
int menu();
// Function to search cereal array by name
void searchByName(string name , const cereal cArr[],const int &cSize , ostream& out);
// Function to swap two cereals in array (for sorting)
void swapCereal(cereal &c1, cereal &c2);
// Function to sort the array on any field
void sortGreatestToLeast(char fieldType , string fieldName, cereal cArr[], const int &cSize);
// Function to get cereal with max or min value
cereal getMaxOrMin(string fieldName , const cereal cArr[], const int &cSize , bool max);

/*
    ifstream inFile("Cereal.txt");
    while(getline(inFile, temp, '\t') >> words) {
    cout << temp << endl;
    }
*/

int main(int argc, char **argv){
    //declaring main strings, array, and cereal size int
    string fName = "";
    cereal cArr[maxSize];
    int cerealSize = 0;

    // If file was provided on command line
    if(argc == 2){  
        fName = argv[1]; 
    }
    // File was not provided on command line
    else{ 
        cout << "Please Enter File Name" << endl;
        cin >> fName;
    //if file hasn't been read in yet, ask for file name
    }   
    while(!readFile(fName, cArr, cerealSize)){
        cout << "Please Enter File Name" << endl;
        cin >> fName;
    }

    //will always run, only get out by inputting 1,2,3,4,5, or 6
    while(true){
        //runs menu function and saves input as integer "select"
        int select = menu();
        if (select == 1) { //if user inputs 1
            string selection;
            cout << "Enter Cereal Name" << endl;
            cin.ignore(); //clears input buffer
            getline(cin, selection);
            searchByName(selection , cArr, cerealSize , cout);
        }
        if (select == 2) { //if user inputs 2
            char type = ' ';
            string field;
            cout << "What is the type of field you are sorting on?" << endl
                 << "   (n)umber" << endl
                 << "   (c)haracter" << endl
                 << "   (s)tring" << endl;
            cin >> type;
            cout << "What field are you sorting on?" << endl;
            cin.ignore(); //clears input buffer
            getline(cin, field);
            sortGreatestToLeast(type , field, cArr, cerealSize);
            cout << "Sorting complete." << endl;
        }
        if (select == 3) { //if user inputs 3
            int type = 0;
            string field;
            bool max = false;
            cout << "Do you want to find the max or the min value?" << endl
                 << "(0) min" << endl
                 << "(1) max" << endl;
            cin >> type;
            //if type chosen is max
            if (type == 1) {
                max = true;
            }
            cout << "What numeric field do you want to look for?" << endl;
            cin.ignore(); //clears input buffer
            getline(cin, field);
            getMaxOrMin(field, cArr, cerealSize, max);
        }
        if (select == 4) { //if user inputs 4
            string userfName;
            cout << "Enter the file name." << endl;
            cin.ignore(); //clears input buffer
            getline(cin, userfName);
            ofstream outFile (userfName);
            printCerealArr(cArr, cerealSize, outFile);
            cout << "Saved to " << userfName << "." << endl;
        }
        if (select == 5) { //if user inputs 5
            printCerealArr(cArr, cerealSize, cout);
        }
        else if(select == 6) { //if user inputs 6
            return 0;
        }
    }
    //main is exited
    return 0;
}

//opens ifstream to read in cereal.txt, one \t at a time
bool readFile(string fName , cereal cArr[], int &cSize) {
    cSize = 0;
    ifstream inFile; 
    inFile.open(fName); //opens stream for file to read
    //if file with fName given can't be opened, give error message and reask for file name
    if(!inFile.is_open()){ 
        cout << "Error: File failed to open." << endl;
        return false;
    }
    cout << "File Opened!" << endl;
    string temp = ""; // Store strings read from file
    getline(inFile, temp); // Header
    while (cSize < maxSize) {
        if(!getline(inFile, temp, '\t')){
            inFile.close();
            return true;
        } 
        //getline(inFile, temp);
        cArr[cSize].name = temp;
        // each array index is entry of struct of type cereal, each array index is just 'cereal' entry that has all variables saved inside
        
        getline(inFile, temp, '\t'); //mfr
        cArr[cSize].mfr = temp[0];  //converted to char by choosing first index of string array

        getline(inFile, temp, '\t'); //type
        cArr[cSize].type = temp[0]; //converted to char by choosing first index of string array

        getline(inFile, temp, '\t'); //calories
        cArr[cSize].calories = stoi(temp);

        getline(inFile, temp, '\t'); //protein
        cArr[cSize].protein = stoi(temp);

        getline(inFile, temp, '\t'); //fat
        cArr[cSize].fat = stoi(temp);

        getline(inFile, temp, '\t'); //sodium
        cArr[cSize].sodium = stoi(temp);

        getline(inFile, temp, '\t'); //fiber
        cArr[cSize].fiber = stof(temp);

        getline(inFile, temp, '\t'); //carbo
        cArr[cSize].carbo = stof(temp);

        getline(inFile, temp, '\t'); //sugars
        cArr[cSize].sugars = stoi(temp);

        getline(inFile, temp, '\t'); //potass
        cArr[cSize].potass = stoi(temp);

        getline(inFile, temp, '\t'); //vitamins
        cArr[cSize].vitamins = stoi(temp);

        getline(inFile, temp, '\t'); //shelf
        cArr[cSize].shelf = stoi(temp);

        getline(inFile, temp, '\t'); //weight
        cArr[cSize].weight = stof(temp);

        getline(inFile, temp, '\t'); //cups
        cArr[cSize].cups = stof(temp);

        getline(inFile, temp, '\n'); //rating
        cArr[cSize].rating = stof(temp);

        //cout << cArr[cSize].name << cArr[cSize].mfr << cArr[cSize].type << cArr[cSize].calories << cArr[cSize].protein << cArr[cSize].fat << cArr[cSize].sodium <<
        //cArr[cSize].fiber << cArr[cSize].carbo << cArr[cSize].sugars << cArr[cSize].potass << cArr[cSize].vitamins << cArr[cSize].shelf <<
        //cArr[cSize].weight << cArr[cSize].cups << cArr[cSize].rating << endl;

        cSize++;
    }
    //closes infile stream so memory leak does not occur
    inFile.close();
    return true;
}

//prints out one index inside cereal array
void printCereal(const cereal &c, ostream &out) {
    out << "Cereal:" << endl
        << "*******************" << endl 
        << "* " << c.name << endl 
        << "*******************" << endl 
        << "* MFR: " << c.mfr << endl
        << "* TYPE: " << c.type << endl
        << "* CALORIES: " << c.calories << endl
        << "* PROTEIN: " << c.protein << endl
        << "* FAT: " << c.fat << endl
        << "* SODIUM: " << c.sodium << endl
        << "* FIBER: " << c.fiber << endl
        << "* CARBO: " << c.carbo << endl
        << "* SUGARS: " << c.sugars << endl
        << "* POTASS: " << c.potass << endl
        << "* VITAMINS: " << c.vitamins << endl
        << "* SHELF: " << c.shelf << endl
        << "* WEIGHT: " << c.weight << endl
        << "* CUPS: " << c.cups << endl
        << "* RATING: " << c.rating << endl
        << "*******************" << endl;
}

//loops through cArr cereal array, and uses printcereal() function to 
//print out all cereals
void printCerealArr(const cereal cArr[], const int &cSize , ostream &out) {
    for(int i = 0; i < cSize; i++){
        printCereal(cArr[i], out);
    }
    cout << endl;
}

//prints out menu and loops until 1-6 is input
int menu(){
    // Loop until proper input
    while(true){
        cout << "--------------------------" << endl
            << "|          Menu           |" << endl
            << "--------------------------" << endl
            << "(1) Search by Name" << endl
            << "(2) Sort Cereal Array" << endl
            << "(3) Find Max or Min Cereal" << endl
            << "(4) Write Cereal Array to File" << endl
            << "(5) Print the Whole Array" << endl
            << "(6) Quit" << endl
            << "--------------------------" << endl;
        string select; //declares select string for input
        cin >> select; //takes in input
        if(select.length() == 1){ // If they enter 1 char
            if(select[0] >= 49 && select[0] <= 54){  //select[0] acts as first char in string, converts string to char
                return select[0] - 48; // Convert char to int
            }
        }
        cout << "Error: Invalid Entry." << endl;
    }
}

//returns queried integer stat about cereal
float getNumber(string fieldName , const cereal &c) {
    //if user queries calories
    if (fieldName == "calories") { 
        return c.calories;
    }
    //if user queries protein
    if (fieldName == "protein") {
        return c.protein;
    }
    //if user queries fat
    if (fieldName == "fat") {
        return c.fat;
    }
    //if user queries sodium
    if (fieldName == "sodium") {
        return c.protein;
    }
    //if user queries fiber
    if (fieldName == "fiber") {
        return c.fiber;
    }
    //if user queries carbo
    if (fieldName == "carbo") {
        return c.carbo;
    }
    //if user queries sugars
    if (fieldName == "sugars") {
        return c.sugars;
    }
    //if user queries potass
    if (fieldName == "potass") {
        return c.potass;
    }
    //if user queries vitamins
    if (fieldName == "vitamins") {
        return c.vitamins;
    }
    //if user queries shelf
    if (fieldName == "shelf") {
        return c.shelf;
    }
    //if user queries weight
    if (fieldName == "weight") {
        return c.weight;
    }
    //if user queries cups
    if (fieldName == "cups") {
        return c.cups;
    }
    //if user queries rating
    if (fieldName == "rating") {
        return c.rating;
    }
    //return with no result
    return -1;
}

//returns queried char stat about cereal
char getChar(string fieldName , const cereal &c) {
    //user searching for mfr
    if (fieldName == "mfr") {
        return c.mfr;
    }
    //user searching for type
    if (fieldName == "type") {
        return c.type;
    }
    return '\0';
}

//returns queried string stat about cereal (name)
string getName(const cereal &c) {
    return c.name;
}

//returns searched cereal if found, prints error if cereal does not exist in cArr array
void searchByName(string name , const cereal cArr[],const int &cSize , ostream& out) {
    bool found = false;
    int index = 0;
    //loops through whole cArr array, and sets bool true if cereal is found
    for (int i = 0; i < cSize; i++) {
        if (cArr[i].name == name) {
            //cout << "Cereal Found: " << name << endl;
            found = true;
            index = i;

        }
    }
    //if cereal wasn't found, found stays equal to false and error message is printed
    if (found == false) {
        cout << "Error: Did not find that cereal." << endl;
    } 
    //if cereal was found, print out cereal index found was set to true at 
    else if (found == true) {
        printCereal(cArr[index], cout);
    }
}

//swaps the spots of two indexes in cArr array
//used in sortGreatestToLeast
void swapCereal(cereal &c1, cereal &c2) {
    cereal temp; 
    temp = c1;
    c1 = c2;
    c2 = temp;
}

//sorts cArr array based on queried statistic
void sortGreatestToLeast(char fieldType, string fieldName, cereal cArr[], const int &cSize) {
    auto comparator = [&](const cereal &a, const cereal &b) -> bool {
        if (fieldType == 's') {
            return a.name > b.name;
        } else if (fieldType == 'c') {
            if (fieldName == "mfr") return a.mfr > b.mfr;
            if (fieldName == "type") return a.type > b.type;
        } else if (fieldType == 'n') {
            if (fieldName == "calories") return a.calories > b.calories;
            if (fieldName == "protein") return a.protein > b.protein;
            if (fieldName == "fat") return a.fat > b.fat;
            if (fieldName == "sodium") return a.sodium > b.sodium;
            if (fieldName == "sugars") return a.sugars > b.sugars;
            if (fieldName == "potass") return a.potass > b.potass;
            if (fieldName == "vitamins") return a.vitamins > b.vitamins;
            if (fieldName == "shelf") return a.shelf > b.shelf;
            if (fieldName == "fiber") return a.fiber > b.fiber;
            if (fieldName == "carbo") return a.carbo > b.carbo;
            if (fieldName == "weight") return a.weight > b.weight;
            if (fieldName == "cups") return a.cups > b.cups;
            if (fieldName == "rating") return a.rating > b.rating;
        }
        return false;
    };

    sort(cArr, cArr + cSize, comparator);
}

//loops through cArr array searching for max/min of queried value
cereal getMaxOrMin(string fieldName , const cereal cArr[], const int &cSize , bool max) {
    cereal maxormin = cArr[0];
    int index = 0;
        if (fieldName == "calories") {
        //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].calories > cArr[i].calories) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].calories < cArr[i].calories) {
                        index = i;
                    }
                }
            }
        }
        //user queries for protein
        else if (fieldName == "protein") {
        //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].protein > cArr[i].protein) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].protein < cArr[i].protein) {
                        index = i;
                    }
                }
            }
        }
        //user queries for fat
        else if (fieldName == "fat") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].fat > cArr[i].fat) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].fat < cArr[i].fat) {
                        index = i;
                    }
                }
            }
        }
        //user queries for sodium
        else if (fieldName == "sodium") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].sodium > cArr[i].sodium) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].sodium < cArr[i].sodium) {
                        index = i;
                    }
                }
            }
        }
        //user queries for sugars
        else if (fieldName == "sugars") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].sugars > cArr[i].sugars) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].sugars < cArr[i].sugars) {
                        index = i;
                    }
                }
            }
        }
        //user queries for potass
        else if (fieldName == "potass") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].potass > cArr[i].potass) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].potass < cArr[i].potass) {
                        index = i;
                    }
                }
            }
        }
        //user queries for vitamins
        else if (fieldName == "vitamins") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].vitamins > cArr[i].vitamins) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].vitamins < cArr[i].vitamins) {
                        index = i;
                    }
                }
            }
        }
        //user queries for shelf
        else if (fieldName == "shelf") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].shelf > cArr[i].shelf) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].shelf < cArr[i].shelf) {
                        index = i;
                    }
                }
            }
        }
        //user queries for fiber
        else if (fieldName == "fiber") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].fiber > cArr[i].fiber) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].fiber < cArr[i].fiber) {
                        index = i;
                    }
                }
            }
        }
        //user queries for carbo
        else if (fieldName == "carbo") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].carbo > cArr[i].carbo) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].carbo < cArr[i].carbo) {
                        index = i;
                    }
                }
            }
        }
        //user queries for weight
        else if (fieldName == "weight") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].weight > cArr[i].weight) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].weight < cArr[i].weight) {
                        index = i;
                    }
                }
            }
        }
        //user queries for cups
        else if (fieldName == "cups") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].cups > cArr[i].cups) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].cups < cArr[i].cups) {
                        index = i;
                    }
                }
            }
        }
        //user queries for rating
        else if (fieldName == "rating") {
            //if looking for min value
            if (max == false) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].rating > cArr[i].rating) {
                        index = i;
                    }
                }   
            }
        //if looking for max value
            if (max == true) {
                for(int i = 0; i < cSize; i++) {
                    if(cArr[index].rating < cArr[i].rating) {
                        index = i;
                    }
                }
            }
        }
        //prints only if user is looking for maximum
    if (max == true){
            cout << "Max Found!" << endl;
        }
        //prints only if user is looking for minimum
    else {
            cout << "Min Found!" << endl;
        }
        //runs printcereal() func on whatever index of array held max/min
    printCereal(cArr[index], cout);
    //returns cArr[] index that held max/min
    return cArr[index];
    }