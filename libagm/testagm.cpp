#include "agm.h"

int main(int argc, char **argv)
{
	AGMModel::SPtr xml(new AGMModel());

	AGMModelConverter::fromXMLToInternal("example.xagm", xml);
}

