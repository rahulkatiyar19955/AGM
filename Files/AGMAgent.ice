#ifndef ROBOCOMPAGMAGENT_ICE
#define ROBOCOMPAGMAGENT_ICE

module RoboCompAGMAgent
{
	enum StateEnum { Starting, Running, Stopped};
	struct StateStruct
	{
		StateEnum state;
		string info;
	};

	struct Parameter
	{
		bool editable;
		string value;
		string type;
	};

	dictionary<string, Parameter> ParameterMap;

	interface AGMAgent
	{
		// Activation and state
		bool activate(ParameterMap params);
		bool deactivate();
		StateStruct getState();

		// Parameter
		ParameterMap getParameters();
		bool setParameters(ParameterMap params);

		// Misc
		void kill();
		int uptime();
		bool reloadConfig();
	};

};

#endif
