#include <iostream>
#include <stdlib.h> 
#include <time.h>
#include <vector>
using namespace std;

vector<int> none_rows;
vector<int> none_cols;
vector<int> mine_rows;
vector<int> mine_cols;
vector<int> available_rows;
vector<int> available_cols;
void find_nones(int board[8][8]){
	for(int i=0;i<8;i++){
		for(int j=0;j<8;j++){
			if(board[i][j] == 0){
				none_rows.push_back(i);
				none_cols.push_back(j);
			}
		}
	}
}

void find_mycells(int board[8][8], int color){
	for(int i=0;i<8;i++){
		for (int j=0;j<8;j++){
			if(board[i][j] == color){
				mine_rows.push_back(i);
				mine_cols.push_back(j);
			}
		}
	}
}

void find_available(int board[8][8], int color){
	int opp_color;
	if(color == 1)	opp_color = 2;
	else	opp_color = 1;
	find_mycells(board, color);
	for(int index = 0;index < mine_rows.size();index++){
		//down
		bool flag = false;
		int row = mine_rows.at(index) + 1;
		int col = mine_cols.at(index);
		while(row < 8 && board[row][col] == opp_color){
			row += 1;
			flag = true;
		}
		if(row < 8 && board[row][col] == 0 && flag){
			available_rows.push_back(row);
			available_cols.push_back(col);
		}
		//up
		flag = false;
		row = mine_rows.at(index) - 1;
		col = mine_cols.at(index);
		while(row >= 0 && board[row][col] == opp_color){
			row -= 1;
			flag = true;
		}
		if(row >= 0 && board[row][col] == 0 && flag){
			available_rows.push_back(row);
			available_cols.push_back(col);
		}
		//right
		flag = false;
		row = mine_rows.at(index);
		col = mine_cols.at(index) + 1;
		while(col < 8 && board[row][col] == opp_color){
			col += 1;
			flag = true;
		}
		if(col < 8 && board[row][col] == 0 && flag){
			available_rows.push_back(row);
			available_cols.push_back(col);
		}
		//left
		flag = false;
		row = mine_rows.at(index);
		col = mine_cols.at(index) - 1;
		while(col >= 0 && board[row][col] == opp_color){
			col -= 1;
			flag = true;
		}
		if(col >= 0 && board[row][col] == 0 && flag){
			available_rows.push_back(row);
			available_cols.push_back(col);
		}
		//up_right
		flag = false;
		row = mine_rows.at(index) - 1;
		col = mine_cols.at(index) + 1;
		while(row >= 0 && col < 8 && board[row][col] == opp_color){
			row -= 1;
			col += 1;
			flag = true;
		}
		if(row >= 0 && col < 8 && board[row][col] == 0 && flag){
			available_rows.push_back(row);
			available_cols.push_back(col);
		}
		//up_left
		flag = false;
		row = mine_rows.at(index) - 1;
		col = mine_cols.at(index) - 1;
		while(row >= 0 && col >= 0 && board[row][col] == opp_color){
			row -= 1;
			col -= 1;
			flag = true;
		}
		if(row >= 0 && col >= 0 && board[row][col] == 0 && flag){
			available_rows.push_back(row);
			available_cols.push_back(col);
		}
		//down_right
		flag = false;
		row = mine_rows.at(index) + 1;
		col = mine_cols.at(index) + 1;
		while(row < 8 && col < 8 && board[row][col] == opp_color){
			row += 1;
			col += 1;
			flag = true;
		}
		if(row < 8 && col < 8 && board[row][col] == 0 && flag){
			available_rows.push_back(row);
			available_cols.push_back(col);
		}
		//down_left
		flag = false;
		row = mine_rows.at(index) + 1;
		col = mine_cols.at(index) - 1;
		while(row < 8 && col >= 0 && board[row][col] == opp_color){
			row += 1;
			col -= 1;
			flag = true;
		}
		if(row < 8 && col >= 0 && board[row][col] == 0 && flag){
			available_rows.push_back(row);
			available_cols.push_back(col);
		}
	}
	
}

void coordinate(int & row , int & col ,int board[8][8] , int color){
	srand (time(NULL));
	find_nones(board);
	find_available(board, color);
	int cell_index = rand()%available_rows.size();
	row = available_rows.at(cell_index);
	col = available_cols.at(cell_index);
}

