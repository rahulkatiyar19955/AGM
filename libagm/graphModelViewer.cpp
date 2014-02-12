#include "graphModelViewer.h"

SymbolNode::SymbolNode(std::string _id, std::string _stype) : osg::Group()
{
	id = _id;
	stype = _stype;

	billboard = new osg::Billboard();
	addChild(billboard);
	billboard->setMode(osg::Billboard::POINT_ROT_EYE);

	osg::StateSet* stateset = new osg::StateSet();
	osg::Image* image = osgDB::readImageFile("texture.png");
	if (image)
	{
		osg::Texture2D* texture = new osg::Texture2D;
		texture->setImage(image);
		texture->setFilter(osg::Texture::MIN_FILTER, osg::Texture::LINEAR);
		stateset->setTextureAttributeAndModes(0,texture, osg::StateAttribute::ON);
	}

	stateset->setMode(GL_LIGHTING, osg::StateAttribute::ON);
	setStateSet(stateset);


	osg::TessellationHints* hints = new osg::TessellationHints;
	hints->setDetailRatio(0.6f);

	sphere = new osg::ShapeDrawable(new osg::Sphere(osg::Vec3(0.0f,0.0f,0.0f),RADIUS), hints);
	billboard->addDrawable(sphere);

	osgText::Font *font = osgText::readFontFile("fonts/arial.ttf");
	osg::Vec4 fontSizeColor(0.0f,0.0f,0.0f,100.0f);
	osg::Vec3 cursor;

	cursor = osg::Vec3(0,-RADIUS,0.52*RADIUS);
	textId = new osgText::Text;
	textId->setFont(font);
	textId->setCharacterSize(90);
	textId->setAxisAlignment(osgText::TextBase::XZ_PLANE);
	textId->setPosition(cursor);
	textId->setColor(fontSizeColor);
	textId->setAlignment(osgText::Text::CENTER_CENTER);
	//text->setFontResolution(100,100);
	textId->setText(id);

	cursor = osg::Vec3(0,-RADIUS,-0.35*RADIUS);
	billboard->addDrawable(textId);
	textType = new osgText::Text;
	textType->setFont(font);
	textType->setCharacterSize(90);
	textType->setAxisAlignment(osgText::TextBase::XZ_PLANE);
	textType->setPosition(cursor);
	textType->setColor(fontSizeColor);
	textType->setAlignment(osgText::Text::CENTER_CENTER);
	//text->setFontResolution(100,100);
	textType->setText(stype);
	billboard->addDrawable(textType);
}

void SymbolNode::setId(std::string str)
{
	textId->setText(str);
}
void SymbolNode::setType(std::string str)
{
	textType->setText(str);
}

void SymbolNode::setPosition(float _x, float _y, float _z)
{
	x = _x;
	y = _y;
	z = _z;
	billboard->setPosition(0, osg::Vec3(x, y, z));
	billboard->setPosition(1, osg::Vec3(x, y, z));
	billboard->setPosition(2, osg::Vec3(x, y, z));
}


GraphModelEdge::GraphModelEdge(std::string _src, std::string _dst, std::string _label, std::map<std::string, SymbolNode *> *_nodeMapId) : osg::Group()
{
	src   = _src;
	dst   = _dst;
	label = _label;
	nodeMapId = _nodeMapId;

	SymbolNode *s1 = (*nodeMapId)[src];
	osg::Vec3 p1 = osg::Vec3(s1->x, s1->y, s1->z);
	SymbolNode *s2 = (*nodeMapId)[dst];
	osg::Vec3 p2 = osg::Vec3(s2->x, s2->y, s2->z);

	osg::Vec3 pInc = p2-p1;
	osg::Vec3 pIncNorm = pInc;
	pIncNorm.normalize();
	p1 = p1 + pIncNorm*RADIUS;
	p2 = p2 - pIncNorm*RADIUS;
	pInc = p2-p1;
	float length = pInc.length();

	osg::Quat quat = quaternionFromInitFinalVector(osg::Vec3(0, 0, 1), p2-p1);
	if (length <= 0.000001)
		throw "1";
	float effectiveLength = length-TIPSIZE;
	printf("length:%f  RADIUS:%f    effective:%f\n", length, RADIUS, effectiveLength);
	osg::Cylinder *line = new osg::Cylinder(((p1+p2)/2.f)-(pIncNorm*TIPSIZE), RADIUS/7, effectiveLength);
	line->setRotation(quat);
	osg::ShapeDrawable* lineDrawable = new osg::ShapeDrawable( line );
	lineDrawable->setColor(osg::Vec4(0.7, 0.7, 0.7, 1));
	osg::Geode* shapeGeode = new osg::Geode();
	shapeGeode->addDrawable( lineDrawable );

	osg::Cone* tip = new osg::Cone(p2-pIncNorm*(TIPSIZE+4), 2.*RADIUS/9., 1.6*TIPSIZE);
	tip->setRotation(quat);
	osg::ShapeDrawable* tipDrawable = new osg::ShapeDrawable(tip);
	lineDrawable->setColor(osg::Vec4(0.7, 0.7, 0.7, 1));
	shapeGeode->addDrawable( tipDrawable );

	addChild(shapeGeode);
}
	

	
	
GraphModelViewer::GraphModelViewer() : osg::Group()
{
}

void GraphModelViewer::addNode(std::string id, std::string stype)
{
	SymbolNode *s;
	s = new SymbolNode(id, stype);
// 	s->setPosition(2*RADIUS, 2*RADIUS, 2*RADIUS);
	addChild(s);

	nodeMapId[id] = s;
	nodeVector.push_back(s);
}

void GraphModelViewer::setNodePosition(std::string id, float x, float y, float z)
{
	nodeMapId[id]->setPosition(x, y, z);
}

void GraphModelViewer::addEdge(std::string src, std::string dst, std::string label)
{
	GraphModelEdge *edge = new GraphModelEdge(src, dst, label, &nodeMapId);
	addChild(edge);
	edges.push_back(edge);
}


