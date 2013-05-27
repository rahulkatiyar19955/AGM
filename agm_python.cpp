// http://www.boost.org/doc/libs/1_53_0/libs/python/doc/tutorial/doc/html/python/exposing.html

#include <boost/python.hpp>

#include "agm.h"

using namespace boost::python;

BOOST_PYTHON_MODULE(libagm)
{
	class_<AGM>("AGM", init<std::string, std::string>())
	 .def("print", &AGM::print)
	;

// 	class_<AGMModel>("AGMModel", init<>())
// 	 .def("clear", &AGMModel::clear)
// 	;

/*	
	class AGMModel
{
	AGMModel(const AGMModel::SPtr &src);
	AGMModel(const AGMModel &src);
	AGMModel& operator=(const AGMModel &src);

	/// SET's
	void clear();
	int32_t insertSymbol(AGMModelSymbol::SPtr s);
	void resetLastId();

	/// GET's
	AGMModelSymbol::SPtr getSymbol(int32_t identif) const;
	int32_t numberOfEdges() const;
	int32_t numberOfSymbols() const;
	int32_t indexOfSymbol(const AGMModelSymbol::SPtr &value, int32_t from=0) const;
	int32_t indexOfFirstSymbolByValues(const AGMModelSymbol &value, int32_t from=0) const;
	int32_t indexOfFirstSymbolByType(const std::string &value, int32_t from=0) const;
	std::vector<AGMModelSymbol::SPtr> getSymbols() const;
	std::vector<AGMModelEdge> getEdges() const;
	AGMModelSymbol::SPtr &symbol(uint32_t index);
	AGMModelEdge &edge(uint32_t index);

	int32_t getIdentifierByName(std::string name) const;
	int32_t getIdentifierByType(std::string type, int32_t i=0) const;
	int32_t getLinkedID(int32_t id, std::string linkname, int32_t i=0) const;
	int32_t getIndexByIdentifier(int32_t targetId) const;

	std::string generatePDDLProblem(const AGMModel::SPtr &target, int32_t unknowns, const std::string domainName, const std::string problemName="problemName") const;

	std::vector<AGMModelSymbol::SPtr> symbols;
	std::vector<AGMModelEdge> edges;

	*/
	
}


