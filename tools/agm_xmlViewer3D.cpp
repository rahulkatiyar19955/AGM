#include <graphModelViewer.h>

int main(int, char **)
{
	GraphModelViewer *graphViewer = new GraphModelViewer();

	graphViewer->addNode("a", "type");
	graphViewer->setNodePosition("a", 0, 0, 0);
	
	graphViewer->addNode("b", "type");
	graphViewer->setNodePosition("b", 0, 0, 4*RADIUS);

	graphViewer->addEdge("a", "b", "link");

	osgViewer::Viewer viewer;
	viewer.setSceneData(graphViewer);
	return viewer.run();
}


