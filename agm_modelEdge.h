#ifndef WORLDMODELEDGE_H
#define WORLDMODELEDGE_H

#include <string>

#include <stdint.h>

#include "agm_model.h"

class AGMModelEdge
{
public:
	AGMModelEdge();
	~AGMModelEdge();
	AGMModelEdge(int32_t a, int32_t b, std::string linking_);
	AGMModelEdge(const AGMModelEdge &src);
	AGMModelEdge& operator=(const AGMModelEdge &src);

	std::string linking;
	std::pair<int32_t, int32_t> symbolPair;

	std::string toString(const AGMModel::SPtr &world) const;
	std::string toString(const AGMModel *world) const;

private:
	void setFrom(const AGMModelEdge &src);
};

#endif
