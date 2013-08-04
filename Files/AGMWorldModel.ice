#ifndef ROBOCOMPAGMWORLDMODELICE_H
#define ROBOCOMPAGMWORLDMODELICE_H

module RoboCompWorldModel
{
	dictionary<string, string> StringDictionary;
	enum BehaviorResultType { InitialWorld, BehaviorBasedModification, BehaviorBasedNumericUpdate, StatusFailTimeout, StatusFailOther, StatusActive, StatusIdle };

	struct GualzruWorldNode
	{
		string nodeType;
		int nodeIdentifier;
		StringDictionary attributes;
	};
	sequence<GualzruWorldNode> NodeSequence;

	struct GualzruWorldEdge
	{
		int a;
		int b;
		string edgeType;
	};
	sequence<GualzruWorldEdge> EdgeSequence;

	struct GualzruWorld
	{
		NodeSequence nodes;
		EdgeSequence edges;
	};

	struct ModelEvent
	{
		string sender;
		BehaviorResultType why;
		GualzruWorld backModel;
		GualzruWorld newModel;
	};

};

#endif
