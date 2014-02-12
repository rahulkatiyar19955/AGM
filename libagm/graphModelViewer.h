#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/Material>
#include <osg/Texture2D>
#include <osgUtil/ShaderGen>

#include <osgViewer/Viewer>

#include <osgDB/ReadFile>
#include <osgDB/WriteFile>

#include <osg/Math>

#include <osgText/Font3D>
#include <osgText/Text>
#include <osgText/Text3D>

#define RADIUS 100.
#define TIPSIZE 40.


#include "agm.h"

class GraphModelViewer;
class GraphModelEdge;

class SymbolNode : public osg::Group
{
friend GraphModelEdge;

public:
	SymbolNode(std::string _id, std::string _stype);
public:
	void setId(std::string str);
	void setType(std::string str);

	void setPosition(float x, float y, float z);

private:
	float x, y, z;
	std::string stype;
	std::string id;

	osgText::Text *textId;
	osgText::Text *textType;
	osg::Billboard *billboard;
	osg::Drawable *sphere;
};


class GraphModelEdge : public osg::Group
{
public:
	GraphModelEdge(std::string _src, std::string _dst, std::string _label, std::map<std::string, SymbolNode *> *_nodeMapId);

public:
	std::string src, dst;
	std::string label;
	std::map<std::string, SymbolNode *> *nodeMapId;

private:
	GraphModelViewer *viewer;
	osg::Quat quaternionFromInitFinalVector(const osg::Vec3 &initV, const osg::Vec3 &destV) const
	{
		osg::Vec3 vQuat = destV^initV;
		const double aQuat = acos(initV * destV);

		if (vQuat.length() > 0.00000001)
		{
			return osg::Quat(-aQuat, vQuat);
		}
		else
		{
			const double aQuat = atan2(destV[2], destV[0]);
			return osg::Quat(-aQuat+M_PIl/2., osg::Vec3(0, 1, 0));
		}
	}
};


class GraphModelViewer : public osg::Group
{
friend GraphModelEdge;
public:
	GraphModelViewer();

	void addNode(std::string id, std::string stype);
	void setNodePosition(std::string id, float x, float y, float z);
	void addEdge(std::string src, std::string dst, std::string label);

private:
	std::map<std::string, SymbolNode *> nodeMapId;
	std::vector<SymbolNode *> nodeVector;

	std::vector<GraphModelEdge *> edges;
};
