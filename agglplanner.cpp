#include "agm.h"

int main(int argc, char **argv)
{
	if (argc < 3)
	{
		printf("Usage %s world goal\n", argv[0]);
		return -1;
	}
	AGMModel::SPtr world(new AGMModel());
	AGMModelConverter::fromXMLToInternal(argv[1], world);
	AGMModel::SPtr goal(new AGMModel());
	AGMModelConverter::fromXMLToInternal(argv[2], goal);

	printf("Goal met: %d\n", AGMSearch::goalIsMet(world, goal));

	return 0;
}

