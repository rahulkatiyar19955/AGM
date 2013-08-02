#pragma once

#include <stdint.h>
#include <stdio.h>

#include <exception>
#include <string>
#include <sstream>

class AGMModelException : public std::exception
{
public:
	AGMModelException(std::string file__, int32_t line__, std::string text__="") throw()
	{
		file_      =      file__;
		line_      =      line__;
		text_      =      text__;
	}
	~AGMModelException() throw()
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

#define AGMMODELEXCEPTION(X) { throw AGMModelException(__FILE__, __LINE__, X); }
