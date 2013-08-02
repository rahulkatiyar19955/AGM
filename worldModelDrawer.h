#ifndef WORLDMODELDRAWER_H
#define WORLDMODELDRAWER_H

#include <QObject>
#include <QTableWidget>

#include <stdlib.h>

#include <worldModel.h>
#include <worldModelEdge.h>
#include <worldModelSymbols.h>

#include <rcdraw/rcdraw.h>


#define SPRING_LENGTH 50.
#define HOOKES_CONSTANT 0.2
#define FRICTION 0.92
#define FIELD_FORCE_MULTIPLIER 60000.


class WorldModelDrawer : QObject
{
Q_OBJECT
public:
	WorldModelDrawer(RCDraw *drawer_, QTableWidget *tableWidget_=NULL)
	{
		drawer = drawer_;
		tableWidget = tableWidget_;
		modified = false;
		connect(drawer, SIGNAL(newCoor(QPointF)), this, SLOT(clickedNode(QPointF)));

	}

	void update(const WorldModel::SPtr &w)
	{
		model = w;
		updateStructure();
		recalculatePositions();
		draw();
		drawer->update();
	}

	void updateStructure()
	{
// 		printf("UPDATING STRUCTURE\n");
		/// Push back new nodes
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
				for (int d=0; d<2; d++)
				{
					node.pos[d] = (100.*rand())/RAND_MAX - 50.;
					node.vel[d] = 0;
				}
				nodes.push_back(node);
			}
		}
		/// Remove deleted nodes
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
		/// Clear edges
		for (uint32_t e=0; e<nodes.size();e++)
		{
			nodes[e].edges.clear();
			nodes[e].edgesOriented.clear();
			nodes[e].edgesNames.clear();
		}
		/// Push back edges again
		for (uint32_t e=0; e<model->edges.size(); e++)
		{
			std::string first  = model->symbols[model->getIndexByIdentifier(model->edges[e].symbolPair.first) ]->toString();
			std::string second = model->symbols[model->getIndexByIdentifier(model->edges[e].symbolPair.second)]->toString();
			int32_t idx1=-1;
			int32_t idx2=-1;
			for (uint32_t n=0; n<nodes.size(); n++)
			{
				if (nodes[n].name == first)
					idx1 = n;
				if (nodes[n].name == second)
					idx2 = n;
			}
			if (idx1 > -1 and idx2 > -1)
			{
				nodes[idx1].edges.push_back(idx2);
				nodes[idx2].edges.push_back(idx1);

				nodes[idx1].edgesOriented.push_back(idx2);
				nodes[idx1].edgesNames.push_back(model->edges[e].linking);
// 				printf("%s -----(%s)-----> %s\n", nodes[idx1].name.c_str(), nodes[idx1].edgesNames.back().c_str(), nodes[nodes[idx1].edgesOriented.back()].name.c_str());
			}
			else
			{
				printf("We had a link whose nodes where not found?!? (%s --> %s)\n", first.c_str(), second.c_str());
				exit(-1);
			}
		}
		modified = true;
	}

	void recalculatePositions()
	{
		static QTime timer = QTime::currentTime();
		float time = double(timer.elapsed())/1000.;
		timer = QTime::currentTime();

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
				float dist2 = pow(pow((abs((i[1]*i[1]) + (i[0]*i[0]))), 0.5), 2.);
				if (dist2 < SPRING_LENGTH)
					dist2 = SPRING_LENGTH;
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
		for (uint32_t n=0; n<nodes.size(); n++)
		{
			for (int d=0; d<2; d++)
			{
				nodes[n].pos[d] += nodes[n].vel[d];
				nodes[n].vel[d] *= 0.94;
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

	void draw()
	{
		const float radius = 20.;
// 		if (modified) printf("DRAWING\n");

		QPointF c = drawer->getWindow().center();
		int wW2 = c.x();
		int wH2 = c.y();

		// Draw links
		for (uint32_t n=0; n<nodes.size(); n++)
		{
			if (modified)
			{
// 				printf("IDENTIFIER %s  index:%d (LINKS:%d,%d)\n", nodes[n].name.c_str(), n, (int)nodes[n].edgesOriented.size(), (int)nodes[n].edgesNames.size());
			}
			for (uint32_t e=0; e<nodes[n].edgesOriented.size(); e++)
			{
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
				drawer->drawText((p1+p2)*0.5, QString::fromStdString(nodes[n].edgesNames[e]), 10, QColor(255));
// 				if (modified) printf("  link[%s] id(%s-->%s) idx(%d-->%d)\n", nodes[n].edgesNames[e].c_str(), nodes[n].name.c_str() , nodes[nodes[n].edgesOriented[e]].name.c_str(), n, nodes[n].edgesOriented[e]);
			}
		}

		// Draw nodes
		for (uint32_t n=0; n<nodes.size(); n++)
		{
			const QPointF p = QPointF(nodes[n].pos[0]+wW2, wH2-nodes[n].pos[1]);
			drawer->drawEllipse(p, radius, radius, QColor(255, 0, 0), true);
			drawer->drawText(p.toPoint(), QString::fromStdString(nodes[n].name), 10, QColor(255));
		}
		modified = false;
// 		printf("\n\n");

		if (tableWidget != NULL) drawTable();
	}

private:
	struct GraphicalNodeInfo
	{
		std::string name;
		std::string type;
		int32_t pos[2];
		float vel[2];
		std::vector<uint32_t> edges;
		std::vector<uint32_t> edgesOriented;
		std::vector<std::string> edgesNames;
	};

private:
	bool modified;
	RCDraw *drawer;
	std::vector<GraphicalNodeInfo> nodes;
	WorldModel::SPtr model;
	QTableWidget *tableWidget;
	std::string interest;

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

