#include <iostream>
#include "AI.cpp"
#include <fstream>
#include "json.hpp"
using namespace std;

// for convenience
using json = nlohmann::json;

int main(){
	////read board from json
	ifstream file("now_board.json");
    json information ;
    file >> information;
	int color = information["color"];
	auto board = information["turn"];
	int myboard[8][8];
	for (int i = 0;i< 8;i++){
		for (int j = 0;j < 8; j++){
			myboard[i][j] = board[i][j];
		}
	}
	file.close();
	///////////
	int row , col;
    coordinate(row , col , myboard , color);
    ////////////////write cordinate in file
    cout << "my choice is: " << row << "," << col << endl;
	ofstream output_file("out.txt");
	output_file << row << " " << col;
	output_file.close();
    return 0;
}