#include <exception>

class WorldModelException : public std::exception
{
public:
	WorldModelException(std::string file__, int32_t line__, std::string text__="") throw()
	{
		file_      =      file__;
		line_      =      line__;
		text_      =      text__;
	}
	~WorldModelException() throw()
	{
	}

	const char* what() const throw()
	{
		std::ostringstream ss;
		ss << file_ << "(" << line_ << "): " << ": Exeception";
		if (text_.size() > 0)
		{
			ss << ": " + text_;
		}
		return ss.str().c_str();
	}

	std::string file_;
	uint32_t line_;
	std::string text_;
	
	std::string file()      { return file_; }
	uint32_t line()         { return line_; }
	std::string text()      { return text_; }
};

#define WORLDMODELEXCEPTION(X) { throw WorldModelException(__FILE__, __LINE__, X); }
