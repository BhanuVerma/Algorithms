/*
CSE6140 HW1
This is an example of how your experiments should look like.
Feel free to use and modify the code below, or write your own experimental code, as long as it produces the desired output.
*/
#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <fstream>

using namespace std;

int main(int argc, char *argv[]) {

	/*
	1. inputs: graph file, change file, name of output file
	2. parseEdges to parse graph file
	3. calculate MST (returns integer, weight of MST); we print this integer to the output file
	4. loop through change file, call function pass in new edge and MST

	*/

	if (argc < 4) {
		cout << "Usage: " << argv[0] << " <graph_file> <change_file> <output_file>" << endl;
		return 1;
	}

	string graph_file = argv[1]; 
	string change_file = argv[2];
	string output_file = argv[3];

	ofstream output;
	output.open(output_file);

	//Write this function to parse edges from graph file to create your graph object
	Graph G = parseEdges(graph_file);

	//Run your MST function on graph G and collect as output the total weight of the MST
	clock_t startMST = clock();
	int MSTweight = computeMST(G);
	clock_t endMST = clock();

	//Subtract the start time from the finish time to get the actual algorithm running time
	clock_t totalTime = 1000 * (endMST - startMST) / (float) CLOCKS_PER_SEC;

	//Write initial MST weight and time to output file
	output << MSTweight << " " << totalTime << endl;

	//Iterate through changes file
	ifstream changes(change_file);
	
	int newMSTWeight = -1;

	if (changes.is_open()) {
		int numChanges;
		changes >> numChanges; //read number of changes

		int counter = 0;
		while (counter < numChanges) {
			int u, v, weight;
			changes >> u; //read u
			changes >> v; //read v
			changes >> weight; //read w(u,v)

			//Run your recomputeMST function to recalculate the new weight of the MST given the addition of this new edge
			//Note: you are responsible for maintaining the MST in order to update the cost without recalculating the entire MST
			clock_t startNewMST = clock();
			newMSTWeight = recomputeMST(u, v, weight, G);
			clock_t endNewMST = clock();

			clock_t totalNewMST = 1000 * (endNewMST - startNewMST) / (float) CLOCKS_PER_SEC;

			//Write new weight and time to output file
			output << newMSTWeight << " " << totalNewMST << endl;

			counter++;
		}
		changes.close();
	}

	output.close();

	return 0;

}