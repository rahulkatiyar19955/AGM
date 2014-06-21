#ifndef WORLDMODELDRAWER_H
#define WORLDMODELDRAWER_H

#include <QObject>
#include <QTableWidget>

#include <stdlib.h>

#include <agm_model.h>
#include <agm_modelEdge.h>
#include <agm_modelSymbols.h>

#include <rcdraw/rcdraw.h>


#define SPRING_LENGTH 50.
#define HOOKES_CONSTANT 0.14
#define FRICTION 0.97
#define FIELD_FORCE_MULTIPLIER 60000.


/*!
 * @brief AGMModel drawing class
 *
 * 
 * 
 */
class AGMModelDrawer : QObject
{
Q_OBJECT
public:
	/// Constructor. It is parametrized with a RCDraw object and an <strong>optional</strong> QTableWidget object (used to show nodes' attributes).
	AGMModelDrawer(RCDraw *drawer_, QTableWidget *tableWidget_=NULL)
	{
		drawer = drawer_;
		drawer->setZoomMultiplier(0.91);
		tableWidget = tableWidget_;
		modified = false;
		connect(drawer, SIGNAL(newCoor(QPointF)), this, SLOT(clickedNode(QPointF)));
	}

	/// This method updates the widget with the current model ('w' vairable).
	void update(const AGMModel::SPtr &w)
	{
		drawer->autoResize();
		mutex.lock();
		model = AGMModel::SPtr(new AGMModel(w));
		updateStructure();
		recalculatePositions();
		draw();
		drawer->update();
		mutex.unlock();
	}

private:
	/// Inspects the current model to detect significant changes.
	void updateStructure()
	{
// printf("%s: %d\n", __FILE__, __LINE__);
		// Push back new nodes
		for (uint32_t e1=0; e1<model->symbols.size(); e1++)
		{
			bool found = false;
			for (uint32_t e2=0; e2<nodes.size(); e2++)
			{
				if (nodes[e2].name == model->symbols[e1]->toString())
				{
					found = true;
					break;
				}
			}
			if (not found)
			{
				GraphicalNodeInfo node;
				node.name = model->symbols[e1]->toString();
				node.type = model->symbols[e1]->symbolType;
				node.identifier = model->symbols[e1]->identifier;
				for (int d=0; d<2; d++)
				{
					node.pos[d] = (100.*rand())/RAND_MAX - 50.;
					node.vel[d] = 0;
				}
				nodes.push_back(node);
			}
		}
// printf("%s: %d\n", __FILE__, __LINE__);
		// Remove deleted nodes
		for (uint32_t e1=0; e1<nodes.size();)
		{
			bool found = false;
			for (uint32_t e2=0; e2<model->symbols.size(); e2++)
			{
				if (nodes[e1].name == model->symbols[e2]->toString())
				{
					found = true;
					break;
				}
			}
			if (not found)
				nodes.erase(nodes.begin() + e1);
			else
				e1++;
		}
// printf("%s: %d\n", __FILE__, __LINE__);
		// Clear edges
		for (uint32_t e=0; e<nodes.size();e++)
		{
			nodes[e].edges.clear();
			nodes[e].edgesOriented.clear();
			nodes[e].edgesNames.clear();
		}
// printf("%s: %d\n", __FILE__, __LINE__);
		// Push back edges again
		for (uint32_t e=0; e<model->edges.size(); e++)
		{
// printf("%s: %d\n", __FILE__, __LINE__);
			int f = model->getIndexByIdentifier(model->edges[e].symbolPair.first);
// printf("%s: %d\n", __FILE__, __LINE__);
			int s = model->getIndexByIdentifier(model->edges[e].symbolPair.second);
// printf("%s: %d\n", __FILE__, __LINE__);
			if (s<0 or f<0)
			{
				printf("%d --> %d\n", model->getIndexByIdentifier(model->edges[e].symbolPair.first), model->getIndexByIdentifier(model->edges[e].symbolPair.second));
				continue;	
			}
// printf("%s: %d\n", __FILE__, __LINE__);
			std::string first  = model->symbols[f]->toString();
			std::string second = model->symbols[s]->toString();
// printf("%s: %d\n", __FILE__, __LINE__);
			int32_t idx1=-1;
			int32_t idx2=-1;
			for (uint32_t n=0; n<nodes.size(); n++)
			{
// printf("%s: %d\n", __FILE__, __LINE__);
				if (nodes[n].name == first)
					idx1 = n;
				if (nodes[n].name == second)
					idx2 = n;
			}
			if (idx1 > -1 and idx2 > -1)
			{
// printf("%s: %d\n", __FILE__, __LINE__);
				nodes[idx1].edges.push_back(idx2);
				nodes[idx2].edges.push_back(idx1);

				nodes[idx1].edgesOriented.push_back(idx2);
				nodes[idx1].edgesNames.push_back(model->edges[e].linking);
			}
			else
			{
// printf("%s: %d\n", __FILE__, __LINE__);
				printf("We had a link whose nodes where not found?!? (%s --> %s)\n", first.c_str(), second.c_str());
				exit(-1);
			}
// printf("%s: %d\n", __FILE__, __LINE__);
		}
// printf("%s: %d\n", __FILE__, __LINE__);
		modified = true;
	}

	/// Move the nodes according to a edges-attraction / nodes-repulsion simulation.
	void recalculatePositions()
	{
		static QTime timer = QTime::currentTime();
		float time = double(timer.elapsed())/1000.;
		timer = QTime::currentTime();
		if (time > 500) time = 500;

		// Compute forces and integrate velocities, storing updated velocities in nodes[n].vel[0-1]
		for (uint32_t n=0; n<nodes.size(); n++)
		{
			int32_t i[2];
			double forceX=0., forceY=0.;
			for (uint32_t n2=0; n2<nodes.size(); n2++)
			{
				if (n == n2) continue;
				for (int d=0; d<2; d++)
					i[d] = nodes[n].pos[d] - nodes[n2].pos[d];
				if (i[0] == 0 and i[1] == 0)
				{
					nodes[n2].pos[0]++;
					nodes[n2].pos[1]++;
					for (int d=0; d<2; d++)
						i[d] = nodes[n].pos[d] - nodes[n2].pos[d];
				}
				float angle = atan2(i[1], i[0]);
				float dist1 = pow((abs((i[1]*i[1]) + (i[0]*i[0]))), 0.5);
				if (dist1 < SPRING_LENGTH)
					dist1 = SPRING_LENGTH;
				float dist2 = pow(dist1, 2.);
				float force = FIELD_FORCE_MULTIPLIER / dist2;
				forceX += force * cos(angle);
				forceY += force * sin(angle);
			}
			for (uint32_t n2=0; n2<nodes.size(); n2++)
			{
				if(std::find(nodes[n].edges.begin(), nodes[n].edges.end(), n2) != nodes[n].edges.end())
				{
					for (int d=0; d<2; d++)
						i[d] = nodes[n].pos[d] - nodes[n2].pos[d];
					float angle = atan2(i[1], i[0]);
					float force = sqrt(abs((i[1]*i[1]) + (i[0]*i[0])));
					if (force <= SPRING_LENGTH) continue;
					force -= SPRING_LENGTH;
					force = force * HOOKES_CONSTANT;
					forceX -= force * cos(angle);
					forceY -= force * sin(angle);
				}
			}
			nodes[n].vel[0] = (nodes[n].vel[0] + (forceX*time))*FRICTION;
			nodes[n].vel[1] = (nodes[n].vel[1] + (forceY*time))*FRICTION;
		}
		// Integrate velocities, storing the result in nodes[n].pos
		// Also, implement friction by multipling velocities by FRICTION
		for (uint32_t n=0; n<nodes.size(); n++)
		{
			for (int d=0; d<2; d++)
			{
				nodes[n].pos[d] += nodes[n].vel[d];
				nodes[n].vel[d] *= FRICTION;
			}
		}

		if (nodes.size() > 0)
		{
			double totalX = 0;
			double totalY = 0;
			for (uint32_t n=0; n<nodes.size(); n++)
			{
				totalX += nodes[n].pos[0];
				totalY += nodes[n].pos[1];
			}
			totalX /= nodes.size();
			totalY /= nodes.size();
			for (uint32_t n=0; n<nodes.size(); n++)
			{
				nodes[n].pos[0] -= totalX;
				nodes[n].pos[1] -= totalY;
			}
		}
	}

	// Actually draw the model in the widget.
	void draw()
	{
		const float radius = 25.;

		QPointF c = drawer->getWindow().center();
		int wW2 = c.x();
		int wH2 = c.y();

		// Draw links
		for (uint32_t n=0; n<nodes.size(); n++)
		{
			if (modified) { /*printf("IDENTIFIER %s  index:%d (LINKS:%d,%d)\n", nodes[n].name.c_str(), n, (int)nodes[n].edgesOriented.size(), (int)nodes[n].edgesNames.size());*/ }
			for (uint32_t e=0; e<nodes[n].edgesOriented.size(); e++)
			{
				int32_t o1 = n;
				int32_t d1 = nodes[n].edgesOriented[e];
				int pos = 0;
				int linkGroupCount = 0;
				for (uint32_t n2=0; n2<nodes.size(); n2++)
				{
					for (uint32_t e2=0; e2<nodes[n2].edgesOriented.size(); e2++)
					{
						if (n==n2 and e==e2)
						{
							pos = linkGroupCount;
						}
						int32_t o2 = n2;
						int32_t d2 = nodes[n2].edgesOriented[e2];
						if ((o1==o2 and d1==d2) or (o1==d2 and d1==o2))
						{
							linkGroupCount += 1;
						}
					}
				}

				QPointF p1 = QPointF(nodes[            n            ].pos[0]+wW2, wH2-nodes[            n            ].pos[1]);
				QPointF p2 = QPointF(nodes[nodes[n].edgesOriented[e]].pos[0]+wW2, wH2-nodes[nodes[n].edgesOriented[e]].pos[1]);
				QPointF inc = (p2 - p1);
				inc /= sqrt(inc.x()*inc.x() + inc.y()*inc.y());
				p1 = p1 + radius*inc;
				p2 = p2 - radius*inc;
				// Link itself
				drawer->drawLine(QLineF(p1, p2), QColor(0, 0, 0));
				// Arrow
				float angle = -atan2(inc.y(), inc.x());
				for (float a = -0.4; a<=0.4; a+=0.05)
				{
					QPointF pr = QPointF(p2.x()-(radius*0.5)*cos(angle+a), p2.y()+(radius*0.5)*sin(angle+a));
					drawer->drawLine(QLineF(p2,  pr), QColor(0, 0, 0));
				}
				// Text
				int32_t linkHeight = 16;
				int32_t linkGroupBase = (-linkGroupCount+1)*linkHeight/2;

				QPointF reLl(0, linkHeight*pos + linkGroupBase);
				drawer->drawText(p1*0.6+p2*0.4-reLl, QString::fromStdString(nodes[n].edgesNames[e]), 10, QColor(255), true, QColor(127,127,127,127));
// 				if (modified) printf("  link[%s] id(%s-->%s) idx(%d-->%d)\n", nodes[n].edgesNames[e].c_str(), nodes[n].name.c_str() , nodes[nodes[n].edgesOriented[e]].name.c_str(), n, nodes[n].edgesOriented[e]);
			}
		}

		// Draw nodes
		for (uint32_t n=0; n<nodes.size(); n++)
		{
			const QPointF p = QPointF(nodes[n].pos[0]+wW2, wH2-nodes[n].pos[1]);
			drawer->drawEllipse(p, radius, radius, QColor(255, 0, 0), true);
			drawer->drawText(p+QPointF(0,-7), QString::fromStdString(nodes[n].type), 10, QColor(255), true);
			drawer->drawText(p+QPointF(0,+10), QString::number(nodes[n].identifier), 10, QColor(255), true);
		}
		modified = false;
// 		printf("\n\n");

		if (tableWidget != NULL) drawTable();
	}

private:
	// Internal representation for nodes.
	struct GraphicalNodeInfo
	{
		std::string name;
		std::string type;
		int32_t identifier;
		int32_t pos[2];
		float vel[2];
		std::vector<uint32_t> edges;
		std::vector<uint32_t> edgesOriented;
		std::vector<std::string> edgesNames;
	};

private:
	bool modified;
	RCDraw *drawer;
	QMutex mutex;
	std::vector<GraphicalNodeInfo> nodes;
	AGMModel::SPtr model;
	QTableWidget *tableWidget;
	std::string interest;

	// Draws attribute table.
	void drawTable()
	{
		int32_t index2 = -1;
		for (uint32_t i=0; i<model->symbols.size(); ++i)
		{
			if (model->symbols[i]->toString() == interest)
			{
				index2 = i;
				break;
			}
		}
		if (index2 != -1)
		{
			std::map<std::string,std::string> &attributes = model->symbols[index2]->attributes;
			tableWidget->setColumnCount(2);
			tableWidget->setRowCount(attributes.size()+1);
			QTableWidgetItem *ti;

			ti = tableWidget->item(0, 0);
			if (ti == NULL) { ti = new QTableWidgetItem(); tableWidget->setItem(0, 0, ti);}
			ti->setText(QString("ID"));

			ti = tableWidget->item(0, 1);
			if (ti == NULL) { ti = new QTableWidgetItem(); tableWidget->setItem(0, 1, ti);}
			ti->setText(QString::fromStdString(model->symbols[index2]->toString()));

			int row = 1;
			for (std::map<std::string,std::string>::iterator iter = attributes.begin(); iter != attributes.end(); iter++, row++)
			{
				ti = tableWidget->item(row, 0);
				if (ti == NULL) { ti = new QTableWidgetItem(); tableWidget->setItem(row, 0, ti);}
				ti->setText(QString::fromStdString( iter->first ));

				ti = tableWidget->item(row, 1);
				if (ti == NULL) { ti = new QTableWidgetItem(); tableWidget->setItem(row, 1, ti);}
				ti->setText(QString::fromStdString( iter->second ));
			}
		}
		else
		{
			if (tableWidget != NULL) tableWidget->clear();
		}
	}


public slots:
	// Updates selected node in the attribute table according to the provided coordinates.
	void clickedNode(QPointF pC)
	{
		if (tableWidget == NULL) return;
		QPointF c = drawer->getWindow().center();
		int wW2 = c.x();
		int wH2 = c.y();
		float x = pC.x();
		float y = pC.y();
		int32_t index = -1;
		float minDist = -1;
		for (uint32_t n=0; n<nodes.size(); n++)
		{
			const QPointF p = QPointF(nodes[n].pos[0]+wW2, wH2+nodes[n].pos[1]);
			const float dist = sqrt( pow(p.x()-x, 2)+pow(p.y()-y, 2));
			if ( dist < 20.)
			{
				if (dist < minDist or minDist < 0)
				{
					index = n;
					minDist = dist;
				}
			}
		}
		if (index > -1)
		{
			interest = nodes[index].name;
		}
	}

};


#endif

