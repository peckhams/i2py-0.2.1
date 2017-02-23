# 
#  Copyright (C) 2005 Christopher J. Stawarz <chris@pseudogreen.org>

#  This file is part of i2py.
# 
#  i2py is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
# 
#  i2py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with i2py; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


"""
Defines classes representing the nodes and leaves of the abstract syntax tree
(AST).  Each such class can produce IDL or Python code for itself via its
__str__() or pycode() method, respectively.
"""


import config
import error
from util import *
import yacc
import map
# import parser  # (SDP)
import re # (SDP)

################################################################################
#
# Abstract base classes
#
################################################################################


class Leaf(object):
   "Base class for leaves of the AST (terminal symbols)"
   pass


class Node(object):
   "Base class for nodes of the AST (nonterminal symbols)"

   # Set of symbols that appear in the RHS of the grammar production for this
   # node
   _symbols = ()

   def __init__(self, prod):
      "Creates a new Node from prod (a yacc.YaccProduction instance)"

      # Validate input (just a sanity check)
      if not isinstance(prod, yacc.YaccProduction):
         raise error.InternalError('expecting YaccProduction, got ' +
	                           prod.__class__.__name__)

      # Store line number and create child_list
      self.lineno = prod.lineno(0)
      self.child_list = list(prod)[1:]
  
      #
      # Create child_dict
      #

      self.child_dict = {}

      for item in prod.slice[1:]:
	 if item.type not in self.child_dict:
	    # No entry for this symbol in child_dict, so make one
            self.child_dict[item.type] = item.value
	 else:
	    # There's already an entry for this symbol in child_dict, so the
	    # entry's value must be a list
	    if isinstance(self.child_dict[item.type], list):
	       # Already a list, so append to it
	       self.child_dict[item.type].append(item.value)
	    else:
	       # Make list from previous and current value
	       self.child_dict[item.type] = ([self.child_dict[item.type],
	                                      item.value])

      # For each valid symbol that isn't involved in this instance, make an
      # entry in child_dict with value None
      for symbol in self._symbols:
         if symbol not in self.child_dict:
	    self.child_dict[symbol] = None

   def __getattr__(self, name):
      """
      Given a symbol name from the right-hand side of the grammar production
      for this node, returns the corresponding child node.  If the production
      includes multiple instances of the symbol, returns a list of their values
      (ordered from left to right).  If the given symbol is not used in the
      current instance, returns None.
      """
      return self.child_dict[name]

   def __getitem__(self, index):
      """
      Returns the child node for the symbol at the corresponding position in
      the right-hand side of the grammar production for this node.  Note that,
      unlike __getattr__, this function only provides access to symbols
      actually used in the current instance.
      """
      return self.child_list[index]

   def __len__(self):
      """
      Returns the number of child nodes in the current instance.  This is
      useful for distinguishing which branch of a grammar production applies to
      the instance.
      """
      return len(self.child_list)

   def __str__(self):
      """
      Returns a string containing the IDL code for the AST rooted at this node.
      """
      return ''.join([ str(child) for child in self ])

   def pycode(self):
      """
      Returns a string containing the Python code for the AST rooted at this
      node.
      """
      return ''.join([ pycode(child) for child in self ])


################################################################################
#
# Terminal symbols
#
################################################################################


class Newline(Leaf):
   def __init__(self, raw):
      rawlines = raw.split('\n')
      rawlines = [rawlines[0]] + [ l.strip() for l in rawlines[1:] ]

      self.lines = []

      for l in rawlines:
	 if l.strip() == '':
	    l = ''
	 else:
	    if l[:1] == '&':
	       l = ' ' + l
	    if l[len(l) - 1] == '&':
	       l = l + ' '
         self.lines.append(l)

   def __str__(self):
      return '\n'.join(self.lines)

   def pycode(self):
      lines = []
      for l in self.lines:
	 if l.strip()[:1] == ';':
	    l = l.replace(';', '#', 1)
	 else:
	    l = l.replace('&', ';')
	    #----------------------------------------
	    # (SDP) How can we add support for line
	    #  continuation character ? (Not this.)
	    #----------------------------------------
	    # l = l.replace('$', '\')
         lines.append(l)
      return '\n'.join(lines)

   def asdocstring(self):
      doc = self.pycode().strip()
      if doc and (doc[:2] == '#+') and (doc[len(doc)-2:] == '#-'):
	 doc = '\n'.join([ l.replace('#', '', 1)
	                   for l in doc.split('\n') ][1:-1])
	 return '"""\n%s\n"""' % doc
      return ''


class Name(Leaf):
   def __init__(self, raw):
      self.raw = raw
   def __str__(self):
      #-----------------------------------------------------------------
      # (SDP) If you like the original mixture of upper and lower
      # case in the IDL variable names, change the next line as shown.
      #-----------------------------------------------------------------
      return self.raw
      # return config.idlnameconv(self.raw)
   def pycode(self):
      vmap = map.get_variable_map(self.raw)
      if vmap:
         return vmap.pyname()
      return pyname(self.raw)


class Number(Leaf):
   def __init__(self, parts):
      self.parts = parts

   def __getattr__(self, name):
      return self.parts[name]

   def __str__(self):
      if self.float:
         return self.float
      return self.integer

   #-------------------------------------------
   # (SDP) Adjustments for 0L, 0b, 0d, etc.
   #  Uses conversion functions in numpy.
   #-------------------------------------------------
   #  In scalar constant assignments, we want to
   #  make sure that the variable becomes a "numpy
   #  object so that we can query its dtype field,
   #  etc.  However, wrapping every 16-bit int with
   #  "int16()" creates a lot of clutter.  So now
   #  we test RHS in class AssignmentStatement.
   #-------------------------------------------------
   def pycode(self):
      num_str = (str(self)).upper()
      # print 'self =', self
      # print 'num_str =', num_str

      value = ''   # (maybe same as self.val)
      code  = ''
      for c in num_str:
         #----------------------------------------------------
         # Hexadecimals and octals may contain single quotes
         #----------------------------------------------------
         if (c.isdigit() or c=='.' or c=='E' or c=='D' or \
             c=='-' or c=='+' or c=="'"):
            value += c
         else:
            code += c

      #------------------------------------------
      # Remove trailing 'D' but keep any inside
      #------------------------------------------
      if (value[-1] == 'D'):
         code  = 'D'
         value = value[:-1]
      
      #-----------------------------------------------
      # If there is no letter code, check the value
      # string for ".", "E" or "D".  If found, use
      # float for "E" or double for "D",
      # otherwise assume it is a 2-byte or "short"
      # integer and set code to "S".
      #-----------------------------------------------
      if (code == ''):
         if   ('D' in value): code = 'D'
         elif ('E' in value): code = 'E'
         elif ('.' in value): code = 'E'
         else: code = 'INTEGER' # (don't wrap with int16())

      # print 'value, code =', value, ',', code
           
      if   (code == 'D'):   s = 'float64(' + value + ')'
      elif (code == 'E'):   s = 'float32(' + value + ')'
      elif (code == 'S'):   s = 'int16('   + value + ')'
      elif (code == 'L'):   s = 'int32('   + value + ')'
      elif (code == 'LL'):  s = 'int64('   + value + ')'
      elif (code == 'B'):   s = 'uint8('   + value + ')'
      elif (code == 'U'):   s = 'uint16('  + value + ')'
      elif (code == 'US'):  s = 'uint16('  + value + ')'           
      elif (code == 'UL'):  s = 'uint32('  + value + ')'
      elif (code == 'ULL'): s = 'uint64('  + value + ')'
      #---------------------------------------
      # Hexadecimal number codes contain "X"
      #---------------------------------------
      elif (code == 'X'):    s = '0x' + value[1:-1].lower()
##      elif (code == 'XB'):   s = '0x' + value[1:-1].lower()
##      elif (code == 'XU'):   s = '0x' + value[1:-1].lower()
##      elif (code == 'XL'):   s = '0x' + value[1:-1].lower()
##      elif (code == 'XUL'):  s = '0x' + value[1:-1].lower()
##      elif (code == 'XLL'):  s = '0x' + value[1:-1].lower()
##      elif (code == 'XULL'): s = '0x' + value[1:-1].lower()
      #----------------------------------------
      # Octal number codes contain 'O' or '"'
      #---------------------------------------- 
##      elif (code == 'O'):    s =
##      elif (code == '"B'):   s =
##      elif (code == '"'):    s = 
##      elif (code == '"U'):   s =
##      elif (code == 'OU'):   s =
##      elif (code == '"L'):   s =
##      elif (code == 'OL'):   s =
##      elif (code == '"L'):   s =
##      elif (code == 'OL'):   s =
##      elif (code == '"UL'):  s =
##      elif (code == 'OUL'):  s =
##      elif (code == '"LL'):  s =
##      elif (code == 'OULL'): s =
      #-----------------------------------------------------
      elif (code == 'INTEGER'): s = value
      else:
         print 'Warning: Unsupported number code: "' + code
         s = value

      return s
   
#---------------------------------------------------------
# (SDP) pycode() method for Number class from I2PY 0.1.0
#---------------------------------------------------------   
##   def pycode(self):
##      
##      if self.float:
##         s = self.dec
##         if self.exp:
##	    s += 'e'
##	    if self.expval:
##	       s += self.expval
##            else:
##	       s += '0'
##      else:
##         if self.val[0] == "'":
##	    if self.val[-1] == 'X':
##	       s = '0x' + self.val[1:-2].lower()
##	    else:
##	       s = self.val[1:-2]
##	       if s[0] != '0':
##	          s = '0' + s
##	 elif self.val[0] == '"':
##	    s = self.val[1:]
##	    if s[0] != '0':
##	       s = '0' + s
##	 else:
##	    s = self.val
##      return s

################################################################################
#
# Nonterminal symbols
#
################################################################################


class TranslationUnit(Node):
   def pycode(self):
      parts = [pycode(self[-1])]

      ec = map.get_extra_code()
      if ec:
         parts.append(ec)

      #---------------------------------------------
      # (SDP) Avoid needing to do it everywhere.
      # Remove extracode cases from "idl_maps.py".
      #---------------------------------------------
      parts.append('import idl_func')
      
      #--------------------------------------------
      # (SDP) Allow inclusion of the module name.
      #--------------------------------------------
      parts.append('import %s' % config.arraymodule)
      
      parts.append('from %s import *' % config.arraymodule)
 
      nl = self.NEWLINE
      if nl:
         doc = nl.asdocstring()
	 if doc:
	    parts.append(doc)
	 else:
            parts[0] = pycode(nl) + parts[0]

      parts.reverse()
      #---------------------------------------
      # (SDP) Use single-spaced import lines
      #---------------------------------------
      return '\n'.join(parts)
      ## return '\n\n'.join(parts)


_in_pro = False
_in_function = False

class SubroutineDefinition(Node):
   def __str__(self):
      return '%s %s' % tuple(self)
   def pycode(self):
      global _in_pro, _in_function

      pars = []
      keys = []

      plist = self.subroutine_body.parameter_list
      if plist:
	 for p in plist.get_items():
	    if p.EXTRA:
	       # FIXME: implement this!
	       error.conversion_error("can't handle _EXTRA yet", self.lineno)
	       return ''
	    if p.EQUALS:
	       keys.append((pycode(p.IDENTIFIER[0]), pycode(p.IDENTIFIER[1])))
	    else:
	       pars.append(pycode(p.IDENTIFIER))

      name = str(self.subroutine_body.IDENTIFIER)
      fmap = map.get_subroutine_map(name)
      if not fmap:
         inpars  = range(1, len(pars)+1)
	 outpars = inpars
	 inkeys  = [ k[0] for k in keys ]
	 outkeys = inkeys

      if self.PRO:
         _in_pro = True
	 if not fmap:
	    fmap = map.map_pro(name, inpars=inpars, outpars=outpars,
	                       inkeys=inkeys, outkeys=outkeys)
      else:
         _in_function = True
	 if not fmap:
	    fmap = map.map_func(name, inpars=inpars, inkeys=inkeys)

      try:
         header, body = fmap.pydef(pars, keys)
      except map.Error, e:
         error.mapping_error(str(e), self.lineno)
	 header, body = '', ''

      body += '\n' + pycode(self.subroutine_body.statement_list)

      #--------------------------------------------------------------
      # (SDP) At this point we're finished adding things to "body".
      # We may therefore be able to scan the IDL statement_list or
      # "body" here in order to find and replace certain patterns.
      #--------------------------------------------------------------
      if self.PRO:
         last = self.subroutine_body.statement_list.get_statements()[-1]
         jump = last.simple_statement and last.simple_statement.jump_statement
         if (not jump) or (not jump.RETURN):
            #--------------------------------------------------
            # (SDP) Added this extra test to avoid adding the
            # "optional return value" (opt_rv) machinery when
            # we don't need it.
            #--------------------------------------------------
            if (fmap.RETURN_LINE != ''):
               body += (fmap.RETURN_LINE + "\n\n")

      nl = self.subroutine_body.NEWLINE[0]
      doc = nl.asdocstring()
      if doc:
         nl = '\n' + pyindent(doc) + '\n\n'
      else:
         nl = pycode(nl)

      _in_pro = False
      _in_function = False

      return (header + nl + pyindent(body) +
              pycode(self.subroutine_body.NEWLINE[1]))


class SubroutineBody(Node):
   def __str__(self):
      if self.parameter_list:
         params = ', ' + str(self.parameter_list)
      else:
         params = ''
      return '%s%s%s%sEND%s' % (self.IDENTIFIER, params, self.NEWLINE[0],
                                indent(self.statement_list), self.NEWLINE[1])


class _CommaSeparatedList(Node):
   def __str__(self):
      if len(self) == 1:
         return str(self[0])
      return '%s, %s' % (self[0], self[2])
   def pycode(self):
      if len(self) == 1:
         return pycode(self[0])
      return '%s, %s' % (pycode(self[0]), pycode(self[2]))
   def get_items(self):
      if len(self) == 1:
         items = [self[0]]
      else:
         items = self[0].get_items()
	 items.append(self[2])
      return items


class ParameterList(_CommaSeparatedList):
   pass


class LabeledStatement(Node):
   def __str__(self):
      if self.NEWLINE:
         return '%s:%s%s' % (self.IDENTIFIER, self.NEWLINE, self.statement)
      return '%s: %s' % (self.IDENTIFIER, self.statement)
   def pycode(self):
      if self.NEWLINE:
         nl = pycode(self.NEWLINE)
      else:
         nl = '\n'
      return '%s:%s%s' % (pycomment(self.IDENTIFIER), nl,
                          pycode(self.statement))


class StatementList(Node):
   def get_statements(self):
      if not self.statement_list:
         stmts = [self.statement]
      else:
         stmts = self.statement_list.get_statements()
	 stmts.append(self.statement)
      return stmts


class IfStatement(Node):
   def __str__(self):
      s = 'IF %s THEN %s' % (self.expression, self.if_clause)
      if self.else_clause:
         s += ' ELSE %s' % self.else_clause
      return s
   
   def pycode(self):
      py_expr = pycode(self.expression)   # (default)
      ##  print '****** py_expr =', py_expr
      
      #---------------------------------------------     
      # (SDP) Clean up the pattern:
      #    "if logical_not((* not in [0,None])):"
      # which results from translating:
      #    "if not(keyword_set(*))..."
      #---------------------------------------------   
      head  = py_expr[:12].lower()
      tail  = py_expr[-17:].lower()
      tail2 = py_expr[-18:].lower()
      if (head == 'logical_not('):
         if (tail == 'not in [0,none]))'):
             arg  = py_expr[13:-18]
             py_expr = "(%s in [0,None])" % arg   
             # We shouldn't need these next 3 lines.
             # arg2 = arg.replace('_','')
             # if (arg2.isalnum()):
             #    py_expr = "(%s in [0,None])" % arg
         elif (tail2 == 'not in [0, none]))'):
             arg  = py_expr[13:-19]
             py_expr = "(%s in [0, None])" % arg
         else:
             #-------------------------------------------
             # Note: logical_not is a NumPy ufunc that
             #       should never appear with "if", but
             #       often appears with "where".
             #-------------------------------------------
             arg = py_expr[12:-1]
             py_expr = "not(%s)" % arg

      #-----------------------------------------------------
      # (SDP) "logical_not", "logical_or" and "logical_and"
      # should not occur in an if statement, so try to
      # replace them.
      #-----------------------------------------------------
      py_expr = py_expr.replace('logical_not(', 'not(')
      
##      while (True):
##         p1 = py_expr.find('logical_')
##         p2 = py_expr.rfind(')')
##         if (p1 == -1) or (p2 == -1):
##            break
##         if (py_expr[p1+8] == 'a'):
##            op = 'and'
##         else:
##            op = 'or'
##         if (p1 != 0):
##            arg0 = py_expr[0:p1]
##         else:
##            arg0 = ''

#----------------------------------------------------------
# Note:  This code doesn't work in general, and actually
#        leads to an infinite loop while translating:
#            "if ((a or b) and (c or d)) then n=0"
#----------------------------------------------------------
##      count = 0
##      while (True):
##         p1 = py_expr.find('logical_')
##         p2 = py_expr.rfind(',')
##         if (p1 == -1) or (p2 == -1):
##            break
##         if (py_expr[p1+8] == 'a'):
##            op = 'and'
##         else:
##            op = 'or'
##         if (p1 != 0):
##            arg0 = py_expr[0:p1]
##         else:
##            arg0 = ''
##         arg1 = py_expr[p1 + len('logical_' + op):p2]
##         arg2 = py_expr[p2+2:]
##         py_expr = '%s%s %s %s' % (arg0, arg1, op, arg2)
##         print 'py_expr =', py_expr
##         count += 1
##         if (count > 4):
##            break
##      print ' '
      
      #-----------------------------------------------------
      # (SDP) Replace a common test that uses "n_elements"
      #     "if (n_elements(**) eq 0)" becomes:
      #     "if not('**' in locals())"
      #-----------------------------------------------------
      # Commented this out because it doesn't work if the
      # argument is a keyword.  Now using a routine called
      # idl_func.n_elements() instead.
      #-----------------------------------------------------
##      IDL_expr    = str(self.expression)     
##      if (IDL_expr[0] == '('):  IDL_expr = IDL_expr[1:]
##      if (IDL_expr[-1] == ')'): IDL_expr = IDL_expr[:-1]
##      head = IDL_expr[0:11].lower()
##      tail = IDL_expr[-6:].lower()
##      if (head == 'n_elements(') and (tail == ') eq 0'):
##         arg  = IDL_expr[11:-6]
##         arg2 = arg.replace('_','')
##         if (arg2.isalnum()):
##            py_expr = "not('%s' in locals())" % arg

      s = 'if %s:%s' % (py_expr, pyindent(self.if_clause).rstrip('\n'))
      if self.else_clause:
         s += '\nelse:%s' % pyindent(self.else_clause).rstrip('\n')
      return s


class _IfOrElseClause(Node):
   def __str__(self):
      if not self.BEGIN:
         return str(self.statement)
      return 'BEGIN%s%s%s' % (self.NEWLINE, indent(self.statement_list),
                              self[-1])
   def pycode(self):
      if not self.BEGIN:
         return '\n' + pycode(self.statement)
      return pycode(self.NEWLINE) + pycode(self.statement_list)

class IfClause(_IfOrElseClause):  pass
class ElseClause(_IfOrElseClause):  pass


class SelectionStatement(Node):
   def pycode(self):
      #------------------------------------------------------------
      # (SDP)  IDL case statements must be converted to Python
      # if-elif-else statements.  A case statement begins with
      # an expression which is then compared to the cases.  In
      # order to avoid repeated evaluation of this expression,
      # i2py-0.1.0 evaluated the expression and saved the result
      # in "_expr".  However, if the expression is really just a
      # variable that doesn't need to be evaluated, this makes
      # the code less readable.  Now we check whether there are
      # any symbols besides letters and numbers in the expression,
      # and if not, we assume it is a variable and can be used
      # directly.  We also allow for a leading symbol like "_".
      #------------------------------------------------------------
      body = self.selection_statement_body
      pbe = pycode(body.expression)
      if (pbe[0] == '(') and (pbe[-1] == ')'):
         pbe = pbe[1:-1]
      is_variable = pbe[1:].isalnum()
      if (is_variable):
         var_name = pbe
         s = ''
      else:
         var_name = 'I2PY_expr'
         s = '%s = %s%s' % (var_name, pbe, pycode(body.NEWLINE))
      #--------------------------   
      if self.CASE:
         is_switch = False
      else:
         is_switch = True
	 s += '_match = False\n'

      cases, actions = body.selection_clause_list.get_cases_and_actions()

      key = 'if'
      first = True
      for c, a in zip(cases, actions):
         #----------------------------------------------------
         # (SDP) Check if c is an explicit string, as often
         # happens in IDL case statements.  If so, make sure
         # it stays that way.
         #----------------------------------------------------
         # print 'case = c =', c
         if ((c[0]=="'") and (c[-1]=="'")) or \
            ((c[0]=='"') and (c[-1]=='"')):
            test = ('(%s == %s)' % (var_name, c))
            ## test = ('%s == %s' % (var_name, c))
         else:
	    test = reduce_expression('(%s)' % c)
	    test = '(%s == %s)' % (var_name, test)
	    ## test = '%s == %s' % (var_name, test)
	    
	 if (not first) and is_switch:
	    test = '_match or (%s)' % test

         s += '%s %s:%s' % (key, test, pyindent(a))

	 if is_switch:
	    s += '%s\n' % pyindent('_match = True')

         if first:
	    if is_switch:
	       key = 'if'
	    else:
	       key = 'elif'
	    first = False

      if body.ELSE:
         s += 'else:%s' % pyindent(body.selection_clause)
      elif not is_switch:
         s += 'else:\n%s' % pyindent("raise RuntimeError('no match found " +
	                               "for expression')")

      return s


class SelectionStatementBody(Node):
   def __str__(self):
      s = ' %s OF%s%s' % (self.expression, self.NEWLINE,
                          indent(self.selection_clause_list))
      if self.ELSE:
         s += indent('ELSE %s' % self.selection_clause)
      return s


class SelectionClauseList(Node):
   def get_cases_and_actions(self):
      if self.selection_clause_list:
         cases, actions = self.selection_clause_list.get_cases_and_actions()
      else:
         cases = []
         actions = []

      cases.append(pycode(self.expression))
      actions.append(pycode(self.selection_clause))

      return (cases, actions)


class SelectionClause(Node):
   def __str__(self):
      if self.BEGIN:
         nl = self.NEWLINE[1]
         stmt = ' BEGIN%s%s   END' % (self.NEWLINE[0],
	                              indent(self.statement_list, 2))
      else:
	 nl = self.NEWLINE
         if self.statement:
            stmt = ' %s' % self.statement
         else:
            stmt = ''
      return ':%s%s' % (stmt, nl)
   def pycode(self):
      if self.statement_list:
         return '%s%s%s' % (pycode(self.NEWLINE[0]),
	                    pycode(self.statement_list).rstrip('\n'),
			    pycode(self.NEWLINE[1]))
      if self.statement:
         return '\n' + pycode(self.statement) + pycode(self.NEWLINE)
      return '\npass' + pycode(self.NEWLINE)


class ForStatement(Node):
   def __str__(self):
      if self.BEGIN:
         stmt = 'BEGIN%s%sENDFOR' % (self.NEWLINE, indent(self.statement_list))
      else:
         stmt = str(self.statement)
      return 'FOR %s DO %s' % (self.for_index, stmt)
   def pycode(self):
      if self.statement:
         body = self.statement
	 nl = '\n'
      else:
         body = self.statement_list
	 nl = pycode(self.NEWLINE)
      return 'for %s:%s%s' % (pycode(self.for_index), nl,
                              pyindent(body).rstrip('\n'))


class ForIndex(Node):
   def __str__(self):
      s = '%s = %s, %s' % (self.IDENTIFIER, self.expression[0],
                           self.expression[1])
      if len(self.expression) == 3:
         s += ', %s' % self.expression[2]
      return s
   
   def pycode(self):
      minval = pycode(self.expression[0])
      maxval = pycode(self.expression[1])
      if len(self.expression) == 3:
         incval = pycode(self.expression[2])
      else:
         incval = '1'

      #--------------------------------------------------------
      # (SDP) What is the purpose of adding parentheses here?
      # NB! If they are removed, we'll need to change the next
      # block of "clean up" code. 
      #--------------------------------------------------------
      maxval = reduce_expression('(%s)+(%s)' % (maxval, incval))

      #--------------------------------------------------
      # (SDP) Clean up appearance of maxval, if possible
      #--------------------------------------------------
      if (maxval[-9:] == '- 1))+(1)'):
         maxval = maxval[2:-9].strip()
      if (maxval[-8:] == '-1))+(1)'):
         maxval = maxval[2:-8].strip()
      #-----------------------------------------
      if (maxval[-15:] == '-int16(1)))+(1)'):
          maxval = maxval[2:-15].strip()
      if (maxval[-16:] == '- int16(1)))+(1)'):
          maxval = maxval[2:-16].strip()
      #-----------------------------------------
      if (maxval[-15:] == '-int32(1)))+(1)'):
          maxval = maxval[2:-15].strip()
      if (maxval[-16:] == '- int32(1)))+(1)'):
          maxval = maxval[2:-16].strip()
      #-----------------------------------------
      if (maxval[-15:] == '-int64(1)))+(1)'):
          maxval = maxval[2:-15].strip()
      if (maxval[-16:] == '- int64(1)))+(1)'):
          maxval = maxval[2:-16].strip()

      #------------------------------------------------------------
      # (SDP) Python's xrange() is faster than its range(),
      # and range() is about 3 times faster than NumPy's arange()
      #------------------------------------------------------------
      if (minval == '0'):
          s = '%s in xrange(%s' % (pycode(self.IDENTIFIER), maxval)
      else:
          s = '%s in xrange(%s, %s' % (pycode(self.IDENTIFIER), minval, maxval)
      if len(self.expression) == 3:
         s += ', %s' % incval

      return s + ')'


class WhileStatement(Node):
   def __str__(self):
      if self.BEGIN:
         stmt = 'BEGIN%s%sENDWHILE' % (self.NEWLINE,
	                               indent(self.statement_list))
      else:
         stmt = str(self.statement)
      return 'WHILE %s DO %s' % (self.expression, stmt)
   def pycode(self):
      if self.statement:
         body = self.statement
	 nl = '\n'
      else:
         body = self.statement_list
	 nl = pycode(self.NEWLINE)
      #--------------------------------------------------
      # (SDP) Clean up "while logical_not("
      # LOGICAL_NOT should not be used in this context,
      # so shorten "logical_not(" to "not(".
      #--------------------------------------------------
      I2PY_expr = pycode(self.expression)
      ## print '****** I2PY_expr =', I2PY_expr
      if (I2PY_expr[:12] == 'logical_not('):
         I2PY_expr = I2PY_expr[8:]
         
      return 'while %s:%s%s' % (I2PY_expr, nl,
                                pyindent(body).rstrip('\n'))


class RepeatStatement(Node):
   def __str__(self):
      if self.BEGIN:
         stmt = 'BEGIN%s%sENDREP' % (self.NEWLINE, indent(self.statement_list))
      else:
         stmt = str(self.statement)
      return 'REPEAT %s UNTIL %s' % (stmt, self.expression)
   def pycode(self):
      if self.statement:
         body = self.statement
	 nl = '\n'
      else:
         body = self.statement_list
	 nl = pycode(self.NEWLINE)
      return 'while True:%s%s\n%s' % (nl, pyindent(body).rstrip('\n'),
				      pyindent('if %s:  break' %
				               pycode(self.expression)))


class SimpleStatement(Node):
   def __str__(self):
      if self.ON_IOERROR:
         return 'ON_IOERROR, %s' % self.IDENTIFIER
      return ' '.join([ str(c) for c in self ])
   def pycode(self):
      if self.COMMON:
	 if (not _in_pro) and (not _in_function):
            error.syntax_error('COMMON outside of PRO or FUNCTION', self.lineno)
	    return ''
         return 'global ' + ', '.join([ pycode(id) for id in
	                                self.identifier_list.get_items()[1:] ])
      if len(self) == 1:
         return Node.pycode(self)
      return pycomment(str(self))


class IdentifierList(_CommaSeparatedList):
   pass


class JumpStatement(Node):
   def __str__(self):
      if self.RETURN and self.expression:
         return 'RETURN, %s' % self.expression
      if self.GOTO:
         return 'GOTO, %s' % self.IDENTIFIER
      return Node.__str__(self)
   def pycode(self):
      if self.GOTO:
         error.conversion_error('cannot convert GOTO statements; please ' +
	                        'remove them and try again', self.lineno)
         return pycomment(str(self))
      if not self.RETURN:
         return str(self[0])   ### (SDP) ###
         # return str(self[0]).lower()
      if _in_pro:
         #-------------------------------------------------------
         # (SDP) This should only get triggered by stray RETURN
         # statements in procedures, as with error conditions.
         # With changes made to "map.py", the function "_ret()"
         # will often be undefined.
         #-------------------------------------------------------
         return 'return -1'
         ####### return 'return _ret()'
      if _in_function:
         return 'return ' + pycode(self.expression)
      error.syntax_error('RETURN outside of PRO or FUNCTION', self.lineno)
      return ''


class ProcedureCall(Node):
   def __str__(self):
      if not self.argument_list:
         return str(self.IDENTIFIER)
      return '%s, %s' % (self.IDENTIFIER, self.argument_list)
   def pycode(self):
      if self.argument_list:
         pars, keys = self.argument_list.get_pars_and_keys()
      else:
         pars = []
         keys = []

      name = str(self.IDENTIFIER)
      fmap = map.get_subroutine_map(name)

      if not fmap:
	 keys = [ '%s=%s' % (k[0], k[1]) for k in keys ]
         return '%s(%s)' % (pycode(self.IDENTIFIER), ', '.join(pars + keys))

      try:
         return fmap.pycall(pars, keys)
      except map.Error, e:
         error.mapping_error(str(e), self.lineno)
	 return ''


class ArgumentList(_CommaSeparatedList):
   def get_pars_and_keys(self):
      pars = []
      keys = []

      for a in self.get_items():
	 if a.EXTRA:
	    # FIXME: implement this!
	    error.conversion_error("can't handle _EXTRA yet", self.lineno)
	    return ''
	 if a.DIVIDE:
	    keys.append((pycode(a.IDENTIFIER), 'True'))
	 elif a.IDENTIFIER:
	    keys.append((pycode(a.IDENTIFIER), pycode(a.expression)))
	 else:
	    pars.append(pycode(a.expression))

      return (pars, keys)


class _SpacedExpression(Node):
   def __str__(self):
      if (len(self) == 2) and (not self.NOT):
         return '%s%s' % tuple(self)
      return ' '.join([ str(c) for c in self ])
   def pycode(self):
      if (len(self) == 2) and (not self.NOT):
         return '%s%s' % (pycode(self[0]), pycode(self[1]))
      return ' '.join([ pycode(c) for c in self ])


class AssignmentStatement(_SpacedExpression):
   def pycode(self):       
      #----------------------------------------------------
      # (SDP) Experimental
      #  Note: len(self) equals 3 for most assignments with
      #  "=", even when RHS contains spaces.
      #----------------------------------------------------  
      if (len(self) == 3) and self.assignment_operator.EQUALS:        
         IDL_LHS = str(self.pointer_expression)
         IDL_RHS = str(self.expression)
         PY_LHS  = pycode(self.pointer_expression)
         PY_RHS  = pycode(self.expression)
         #-----------------------------------------------
         # (SDP) Clean up translation of WHERE function
         #-----------------------------------------------
         if ('I2PY_w = ' in PY_RHS):
            PY_RHS = PY_RHS.replace('I2PY_w = ', '')
            PY_RHS = PY_RHS.replace('I2PY_w', PY_LHS)
            return (PY_LHS + ' = ' + PY_RHS)
         #--------------------------------------------------
         # (SDP) Clean up translation of STRSPLIT function   
         #--------------------------------------------------
         if ('I2PY_words = ' in PY_RHS):
            PY_RHS = PY_RHS.replace('I2PY_words = ', '')
            PY_RHS = PY_RHS.replace('I2PY_words', PY_LHS)
            return (PY_LHS + ' = ' + PY_RHS)
         #---------------------------------------------------------
         # (SDP) Clean up translation of DIALOG_PICKFILE function   
         #---------------------------------------------------------
         if ('I2PY_filepath = ' in PY_RHS):
            PY_RHS = PY_RHS.replace('I2PY_filepath = ', '')
            PY_RHS = PY_RHS.replace('I2PY_filepath', PY_LHS)
            return (PY_LHS + ' = ' + PY_RHS)
         #-----------------------------------------------------
         # (SDP) Clean up translation of FILE_SEARCH function   
         #-----------------------------------------------------
         if ('I2PY_file_list = ' in PY_RHS):
            PY_RHS = PY_RHS.replace('I2PY_file_list = ', '')
            PY_RHS = PY_RHS.replace('I2PY_file_list', PY_LHS)
            return (PY_LHS + ' = ' + PY_RHS)
         #-----------------------------------------------
         # (SDP) Clean up translation of FSTAT function   
         #-----------------------------------------------
         if ('I2PY_temp = ' in PY_RHS):
            PY_RHS = PY_RHS.replace('I2PY_temp = ', '')
            PY_RHS = PY_RHS.replace('I2PY_temp', PY_LHS)
            return (PY_LHS + ' = ' + PY_RHS)
         #------------------------------------------------
         # (SDP) Clean up translation of PRINT & PRINTF   
         #------------------------------------------------
         if ('I2PY_out_str = ' in PY_RHS):
            PY_RHS = PY_RHS.replace('I2PY_out_str = ', '')
            PY_RHS = PY_RHS.replace('I2PY_out_str', PY_LHS)
            return (PY_LHS + ' = ' + PY_RHS)
         #--------------------------------------------------------
         # (SDP) Allow scalar string to be added to string array   
         #--------------------------------------------------------
         if (PY_RHS[:6]=="zeros(") and ("dtype='|S100') +" in PY_RHS):
            pos = PY_RHS.find("+")
            scalar_str = PY_RHS[pos+2:]
            PY_RHS = PY_RHS[:pos]
            cmds  = (PY_LHS + ' = ' + PY_RHS + "\n")
            cmds += (PY_LHS + '.fill(' + scalar_str + ')')
##            cmds += 'for I2PY_index in xrange(len(' + PY_LHS + ')):\n'
##            cmds += '    ' + PY_LHS + '[I2PY_index] += ' + scalar_str
            return cmds
         #--------------------------------------
         # (SDP) Clean up increments with "+="   
         #--------------------------------------
         index = len(PY_LHS) + 3
         if (PY_RHS[0:index] == PY_LHS + " + "):
             PY_RHS = PY_RHS[index:]
             return (PY_LHS + " += " + PY_RHS)
         #----------------------------------------------
         index = len(PY_LHS) + 4
         if (PY_RHS[0:index] == '(' + PY_LHS + " + "):
             PY_RHS = PY_RHS[index:-1]
             return (PY_LHS + " += " + PY_RHS)
         #----------------------------------------------------
         # (SDP) Clean up calls to functions in numpy.random
         # that require line to be inserted before this one.
         #----------------------------------------------------
         p1 = PY_RHS.find('I2PY_BEGIN')
         p2 = PY_RHS.find('I2PY_END')
         if (p1 != -1) and (p2 != -1):    
            line1 = PY_RHS[p1+10:p2]
            line2 = PY_LHS + ' = ' + PY_RHS[0:p1] + PY_RHS[p2+8:]
            return (line1 + "\n" + line2)
         #----------------------------------------------
##         print 'IDL_LHS =', IDL_LHS
##         print 'IDL_RHS =', IDL_RHS
##         print 'PY_LHS  =', PY_LHS
##         print 'PY_RHS  =', PY_RHS
##         print 'len(self) =', len(self)
##         print ' '
         #-------------------------------------------------
         #  In scalar constant assignments, we want to
         #  make sure that the variable becomes a numpy
         #  object so that we can query its dtype field,
         #  etc.  However, wrapping every 16-bit int with
         #  "int16()" creates a lot of clutter.  So now
         #  we test RHS in class AssignmentStatement.
         #-------------------------------------------------
         if (IDL_RHS.isdigit()):
            PY_RHS = 'int16(' + IDL_RHS + ')'
##            print 'IDL_RHS =', IDL_RHS
##            print 'PY_RHS  =', PY_RHS
            return (PY_LHS + ' = ' + PY_RHS)
         
         #----------------------------------------------
         if (IDL_RHS.lower() == '(byte(1, 0, 2))[0] eq 0b'):
            PY_RHS = "(sys.byteorder == 'big')"
            return (PY_LHS + ' = ' + PY_RHS)
            # return _SpacedExpression.pycode(self)
         elif (IDL_RHS[0:6] == 'where('):
            return _SpacedExpression.pycode(self)
         else:
            return _SpacedExpression.pycode(self)
         
      #-------------------------------------------------------------      
      if (len(self) == 1) or self.assignment_operator.EQUALS:       
         return _SpacedExpression.pycode(self)

      op = self.assignment_operator.OP_EQUALS
      lvalue = pycode(self.pointer_expression)
      rvalue = pycode(self.expression)

      if op == '#=':
         return (('%s = transpose(matrixmultiply(transpose(%s), ' +
	          'transpose(%s)))') % (lvalue, lvalue, rvalue))

      augops = {'AND=':'&=', 'MOD=':'%=', 'XOR=':'^=', 'OR=':'|=', '+=':'+=',
                '-=':'-=', '*=':'*=', '/=':'/=', '^=':'**='}
      binops = {'EQ=':'==', 'GE=':'>=', 'GT=':'>', 'LE=':'<=', 'LT=':'<',
                'NE=':'!='}
      funcops = {'##=':'matrixmultiply', '<=':'minimum', '>=':'maximum'}

      if op in augops:
         return '%s %s %s' % (lvalue, augops[op], rvalue)
      if op in binops:
         return '%s = %s %s %s' % (lvalue, lvalue, binops[op], rvalue)
      return '%s = %s(%s, %s)' % (lvalue, funcops[op], lvalue, rvalue)


class IncrementStatement(Node):
   def pycode(self):
      if self.PLUSPLUS:
         op = '+'
      else:
         op = '-'
      return '%s %s= 1' % (pycode(self.pointer_expression), op)


class Expression(Node):
   def pycode(self):
      if self.assignment_statement:
         # FIXME: implement this!
         error.conversion_error("can't handle assignment in expressions yet",
	                        self.lineno)
         return ''
      #-------------------------------------------------------------
      # (SDP) Search for cases of "\'", e.g. in Windows pathnames.
      # Put something like this in AssignmentStatement instead ?
      #-------------------------------------------------------------
      ### self = re.subn(r"\'", r"\\'", self)[0]
      # expr = self
##      expr = str(self)
##      # print 'expr =', expr
##      if (re.search(".*\'.*", expr)):
##         print 'Making replacement #################'
##         print 'expr =', expr
##         expr = expr.replace(r"\'", r"\\\'")
##         ## re.subn(r"\'", r"\\'", expr)
##         print 'new_expr =', expr
         
         # self = expr.replace(r"\'", r"\\'")
##      if (re.search('.*\".*', expr)):
##          self = expr.replace(r'\"', r'\\"')

        
      return Node.pycode(self)


class ConditionalExpression(_SpacedExpression):
   def pycode(self):
      if not self.QUESTIONMARK:
         return _SpacedExpression.pycode(self)
      return ('((%s) and [%s] or [%s])[0]' %
              (pycode(self.logical_expression), pycode(self.expression),
	       pycode(self.conditional_expression)))


class LogicalExpression(_SpacedExpression):
   def pycode(self):
      if len(self) == 1:
         return _SpacedExpression.pycode(self)
      if self.TILDE:
         return 'logical_not(%s)' % pycode(self[1])
      if self.AMPAMP:
         op = 'and'
      else:
         op = 'or'
      return 'logical_%s(%s, %s)' % (op, pycode(self.logical_expression),
                                     pycode(self.bitwise_expression))


class BitwiseExpression(_SpacedExpression):
   def pycode(self):
      if len(self) == 1:
         return _SpacedExpression.pycode(self)
      if self.AND:
         op = 'and'
      elif self.OR:
         op = 'or'
      else:
         op = 'xor'
      return 'logical_%s(%s, %s)' % (op, pycode(self.bitwise_expression),
                                     pycode(self.relational_expression))
      #---------------------------------------------------
      # (SDP) This is not usually what we want in IDL.
      #       "logical_%s" seems to be a better default.
      #---------------------------------------------------
##      return 'bitwise_%s(%s, %s)' % (op, pycode(self.bitwise_expression),
##                                     pycode(self.relational_expression))


class RelationalExpression(_SpacedExpression):
   def pycode(self):
      if len(self) == 1:
         return _SpacedExpression.pycode(self)
      if self.EQ:
         op = '=='
      elif self.NE:
         op = '!='
      elif self.LE:
         op = '<='
      elif self.LT:
         op = '<'
      elif self.GE:
         op = '>='
      else:
         op = '>'
      return '%s %s %s' % (pycode(self.relational_expression), op,
                           pycode(self.additive_expression))


class AdditiveExpression(_SpacedExpression):
   def pycode(self):
      if (len(self) == 1) or self.PLUS or self.MINUS:
         return _SpacedExpression.pycode(self)
      if self.NOT:
         #-----------------------------------------------------------------
         # (SDP) This is activated for expressions like "not(DONE)".
         # Almost always want "numpy.logical_not" vs. "numpy.bitwise_not".
         # Recall that Python's "not" cannot handle array arguments, but
         # numpy.logical_not *can* handle scalar arguments.
         # Now there is no case that converts to "bitwise_not".
         #-----------------------------------------------------------------
         s = pycode(self.multiplicative_expression)
         if (s[0] == '(') and (s[-1]==')'): s = s[1:-1]
         return 'logical_not(%s)' % s
         #----------------
         # Original code
         #----------------
         # return 'bitwise_not(%s)' % pycode(self.multiplicative_expression)
      if self.LESSTHAN:
         f = 'minimum'
      else:
         f = 'maximum'
      return '%s(%s, %s)' % (f, pycode(self.additive_expression),
                             pycode(self.multiplicative_expression))


class MultiplicativeExpression(_SpacedExpression):
   def pycode(self):
      if len(self) == 1:
         return _SpacedExpression.pycode(self)
      if self.POUND:
         return ('transpose(matrixmultiply(transpose(%s), transpose(%s)))' %
	         (pycode(self.multiplicative_expression),
		 pycode(self.exponentiative_expression)))
      if self.POUNDPOUND:
         return ('matrixmultiply(%s, %s)' %
	         (pycode(self.multiplicative_expression),
		 pycode(self.exponentiative_expression)))
      if self.TIMES:
         op = '*'
      elif self.DIVIDE:
         op = '/'
      else:
         op = '%'
      return '%s %s %s' % (pycode(self.multiplicative_expression), op,
                           pycode(self.exponentiative_expression))


class ExponentiativeExpression(_SpacedExpression):
   def pycode(self):
      if len(self) == 1:
         return _SpacedExpression.pycode(self)
      return '%s ** %s' % (pycode(self.exponentiative_expression),
                           pycode(self.unary_expression))


class UnaryExpression(Node):
   def pycode(self):
      if self.increment_statement:
         # FIXME: implement this!
         error.conversion_error("can't handle ++,-- in expressions yet",
	                        self.lineno)
         return ''
      return Node.pycode(self)

#------------------------------------
# (SDP)  Added support for pointers
#--------------------------------------------
# NB! Expression has already been identified
# as a PointerExpression, so remove "*" at
# beginning and maybe extra parentheses.
#----------------------------------------------------
# NB! "(*var)[k]" converts to (var)[k], which is OK.
#----------------------------------------------------
# e.g. self[0] = '*' and self[1]='T_AIR'
#----------------------------------------------------
class PointerExpression(Node):
   def pycode(self):
      if self.TIMES:
##         print 'self =', self
##         print 'self[0] =', self[0]
##         print 'self[1] =', self[1]
         var_name = str(self[1])
         # var_name = var_name.lower()  ### (SDP) Avoid this.
         #--------------------------------------------------
         # (SDP) Strip off unneeded, enclosing parentheses
         #--------------------------------------------------
         if (var_name[0] == '(') and (var_name[-1] == ')'):
            var_name = var_name[1:-1]
         return var_name
      
##         if (self[0] == '*') and var_name[0].isalpha():
##            return var_name
##         else:
##            return Node.pycode(self)
      else:
         return Node.pycode(self)

#------------------------------------------------
# (SDP) PointerExpression class from I2PY 0.1.0
#------------------------------------------------   
##class PointerExpression(Node):
##   def pycode(self):
##      if self.TIMES:
##         # FIXME: implement this!
##         error.conversion_error("can't handle pointers yet", self.lineno)
##         return ''
##      return Node.pycode(self)


class PostfixExpression(Node):
   def pycode(self):
      if self.DOT and self.LPAREN:
         # FIXME: implement this!
         #------------------------------------------------------------
         # (SDP) According to Guido's Python tutorial (ch. 9),
         # "there is no shorthand for referencing data attributes".
         #------------------------------------------------------------
         #  However, we are using the "bunch" function to convert
         #  the IDL structures to Python.  This allows us to replace
         #  the IDL code: y = x.(k) with the Python code:
         #     y = x.__dict__.values()[k]
         #  For example:
         #     c = array((3,4))
         #     x = bunch(a=5.0, b=c)
         #     print x.__dict__.values()[0]
         #------------------------------------------------------------
         #  Or we could rewrite the "bunch" function so that it
         #  automatically includes an "index_map" field as in:
         #     x = bunch(a=5.0, b=10.0, imap={0:'a', 1:'b'}).
         #  Then, replace IDL code: "y = x.(0)" with Python code:
         #  y = eval('x.' + x.imap[0]).
         #------------------------------------------------------------
         s = str(self)
         w = s.split('.')
         w0 = w[0].lower()
         w1 = w[1].replace('(','[')
         w1 = w1.replace(')',']')
         s = ''.join((w0,'.__dict__.values()', w1))
         return s

##         error.conversion_error("can't handle '<struct>.(<field_index>)' yet",
##	                        self.lineno)
##         return ''

      #---------------------------------------------------------
      #  (SDP) This works, but is this the best place for it?
      #---------------------------------------------------------
      self_str = str(self).upper()
      ## print 'self_str =', self_str ########
      if (self_str == '!VALUES.F_INF'): return 'float32(numpy.Infinity)'
      if (self_str == '!VALUES.F_NAN'): return 'float32(numpy.NaN)'
      if (self_str == '!VALUES.D_INF'): return 'float64(numpy.Infinity)'
      if (self_str == '!VALUES.D_NAN'): return 'float64(numpy.NaN)'
      
      if (self_str == '!VERSION.OS'):   return 'platform.system()'
      if (self_str == '!VERSION.OS_FAMILY'):
         return "('Windows' if (platform.system()=='Windows') else 'UNIX')"
      if (self_str == '!VERSION.ARCH'): return 'platform.machine()'   
##      if (self_str == '!VERSION.RELEASE'): return
      
      if (self_str == '!D.NAME'):       return 'idl_func.device_name()'
##      if (self_str == '!D.NAME'):
##         return "('WIN' if (platform.system()=='Windows') else 'X'"
      
      if self.DOT or (not self.IDENTIFIER):
##         print 'self=', self
##         print 'self.IDENTIFIER =', self.IDENTIFIER
##         print '--------------------------------------'
         return Node.pycode(self)

      if self.argument_list:
         pars, keys = self.argument_list.get_pars_and_keys()
      else:
         pars = []
         keys = []

      name = str(self.IDENTIFIER)
      fmap = map.get_subroutine_map(name)

      if not fmap:
	 keys = [ '%s=%s' % (k[0], k[1]) for k in keys ]
         return '%s(%s)' % (pycode(self.IDENTIFIER), ', '.join(pars + keys))

      try:
         return fmap.pycall(pars, keys)
      except map.Error, e:
         error.mapping_error(str(e), self.lineno)
	 return ''


class PrimaryExpression(Node):
   def pycode(self):
      if self.LBRACE:
         #----------------------------------------------------
         # (SDP) Convert an IDL structure to a "bunch", as
         #  defined in "idl_func.py".
         #----------------------------------------------------
         #  This simple approach works, and ensures that
         #  expressions within the structure get translated.
         #----------------------------------------------------
         #  If structure is named, remove the name first.
         #----------------------------------------------------
         pc = Node.pycode(self)  # convert inner expressions
         parts = pc.split(',')
         if (":" not in parts[0]): parts = parts[1:]
         pc = ','.join([p for p in parts])
         #----------------------------------
         # print 'pc =', pc
         pc = pc.replace(':','=')
         pc = pc.replace('{','')
         pc = pc.replace('}','')
         # print 'pc =', pc
         cmd = 'idl_func.bunch(' + pc + ')'
         # print 'cmd =', cmd
         # print ' '
         return cmd
      
         #-------------------------------------------        
         # Idea:  Treat RHS as a primary expression
         # and then use Node.pycode(self) ??
         #-------------------------------------------
##         for p in parts:
##            pair = p.split('=')
##            name = pair[0]
##            self.expression = pair[1]
##            py_code = Node.pycode(self)
####            arg = PrimaryExpression(pair[1])
####            py_code = Node.pycode(arg)
##            # py_code = Node.pycode(pair[1])
##            new_str += name + '=' + py_code + ','
               
         #-----------------------------------------------------
         # Use pycode() to translate each AssignmentStatement
         #-----------------------------------------------------         
##         for p in parts:
##            # ppp = AssignmentStatement(p)
##            # py_code = ppp.pycode(ppp)
##            py_code = pycode(p)
##            new_str += py_code + ','
          
##         new_str = new_str[0:len(new_str)-1]   # remove last ","
##         new_str = new_str.replace(' ','')     # remove spaces
##         new_str = new_str.replace(',', ', ')  # add spaces

         # print 'new_str =', new_str  ##########
         
         # return ('bunch(' + new_str + ')')
              
##         words = s.split(',')
##         if (":" not in words[0]):
##            s0 = ','.join(words[1:])
##            s  = '(' + s0.strip()        # (remove leading space)
##
##         s = s.replace('0L','int32(0)')   #
##         s = s.replace('0l','int32(0)')   #
##         s = s.replace('0b','uint8(0)')   # (often means "False")
##         s = s.replace('1b','uint8(1)')   # (often means "True")
##         s = s.replace('0B','uint8(0)')   # (often means "False")
##         s = s.replace('1B','uint8(1)')   # (often means "True")
##         s = s.replace('0d','float64(0)') #
##         s = s.replace('0D','float64(0)') #
##         s = s.replace(':', '=')
##         s = s.replace('{', '(')
##         s = s.replace('}', ')')
##         return ('bunch' + s)
                  

      if self.LBRACKET:
         #--------------------------------------------------------
         # (SDP) IDL uses square brackets for:
         #     (1) creating an array from a comma-separated
         #            list of values, 
         #     (2) concatenating multiple arrays or appending
         #            scalars to an array
         #     (3) creating high-dimensional arrays from vectors
         #     (4) subscripting arrays
         # Consider these examples:
         #     IDL> w = [1,2]
         #     IDL> a = [w, 3,4]
         #     IDL> b = [w, [3,4]]
         #     IDL> c = [[w], [3,4]]
         #     IDL> d = [[w],[w]]
         # The first line shows (1), the 2nd and 3rd lines show
         # (2) -- leading to a 1D array -- and the 4th and 5th
         # lines show (3).  An extra set of brackets enclosing
         # a named variable is needed in order for IDL to create
         # a higher-dimensional array.  Without them, the arrays
         # are concatenated. For example,
         #     IDL> a = [1,2,3]
         #     IDL> b = [4,5,6]
         #     IDL> c = [a, b]     ;(concatenates)
         #     IDL> d = [[a],[b]]  ;(creates 2D array)
         #--------------------------------------------------------
         # In NumPy, numpy.array() is used to create an array
         # from a list of elements, and numpy.concatenate() is
         # used to join two arrays.
         #--------------------------------------------------------
         # If we try:
         #    >>> np.concatenate([1,2,3])
         # we get the error message:
         #    "ValueError: 0-d arrays can't be concatenated"
         #--------------------------------------------------------
         # If we try:
         #    >>> w = np.array([1,2])
         #    >>> a = np.array(w,[1,2])
         # we get the error message:
         #    "TypeError: data type not understood"
         #-------------------------------------------------------------
         # If we try:
         #    >>> w = np.array([1,2])
         #    >>> a = np.array([w,1,2])
         # we get the error message:
         #    "ValueError: setting an array element with a sequence."
         #-------------------------------------------------------------
         
         #----------------------------------------------------------
         # (SDP) Old approach.  We usually want "numpy.array()"
         # instead of "numpy.concatentate()", but issue a warning.
         #----------------------------------------------------------
##         s = Node.pycode(self)
##         print 'Warning: Unsure about square brackets. Assumed array().'      
##         return ('array(%s)' % s)
      
         #------------------------------------------------------
         # (SDP)  Try to distinguish between and correctly
         # translate all cases of array() and concatenate().
         # This now handles all test cases in "i2py_test.pro".
         #------------------------------------------------------
         PY_CODE  = Node.pycode(self)
         IDL_EXPR = str(self)
         pos = IDL_EXPR.find(',')
         if (pos == -1):
            # return PY_CODE
            return ('array(%s)' % PY_CODE)
         #-------------------------------------------------
         # Clip outer square brackets for remaining tests
         # Also remove all blank spaces. (Important)
         #-------------------------------------------------
         str1 = IDL_EXPR[1:-1].replace(' ','')
         NO_MORE_BRACKETS = (str1.count('[') == 0)
         words = str1.split(',')
         #--------------------------------------------------
         # If there are no more brackets and EACH entry
         # starts with a digit (e.g. 72B, 50L, 100D), then
         # we must be creating an array of numbers.
         #--------------------------------------------------
         if (NO_MORE_BRACKETS):
            ALL_NUMBERS = True
            IS_BYTE     = True
            IS_SHORT    = True
            IS_LONG     = True
            IS_LONG64   = True
            IS_DOUBLE   = True
            for w in words:
               ALL_NUMBERS = ALL_NUMBERS and (w[0].isdigit())
               last_char   = w[-1].upper()
               last_two    = w[-2:].upper()
               IS_BYTE     = IS_BYTE   and (last_char == 'B')
               IS_SHORT    = IS_SHORT  and (last_char == 'S')
               IS_LONG     = IS_LONG   and (last_char == 'L')
               IS_LONG64   = IS_LONG64 and (last_two  == 'LL')
               IS_DOUBLE   = IS_DOUBLE and (last_char == 'D')
            if (ALL_NUMBERS):
               #-----------------------------------------------
               # Note that dtype of array([1,2,3]) is "int32".
               # Also, if we use float32([1,2,3]), etc., then
               # result is an ndarray even w/o "array()".
               #-----------------------------------------------               
               cmd = 'int16(%s)'
               if (IS_BYTE):
                  IDL_EXPR = IDL_EXPR.replace('B','')
                  cmd = 'uint8(%s)'
               if (IS_SHORT):
                  IDL_EXPR = IDL_EXPR.replace('S','')
                  cmd = 'int16(%s)'
               if (IS_LONG):
                  if (IS_LONG64):
                     IDL_EXPR = IDL_EXPR.replace('LL','')
                     cmd = 'int64(%s)'
                  else:
                     IDL_EXPR = IDL_EXPR.replace('L','')
                     cmd = 'int32(%s)'
               if (IS_DOUBLE):
                  IDL_EXPR = IDL_EXPR.replace('D','')
                  cmd = 'float64(%s)'
               pos1 = IDL_EXPR.find('.')
               pos2 = IDL_EXPR.find('E')
               IS_FLOAT = (pos1 != -1) or (pos2 != -1)
               if (IS_FLOAT):
                  cmd = 'float32(%s)'
               return (cmd % IDL_EXPR)
               # return (cmd % PY_CODE)
         #--------------------------------------------------
         # If there are no more brackets and EACH entry
         # starts with a quote (e.g. 'x' or "y"), then
         # we must be creating an array of scalar strings.
         #--------------------------------------------------
         if (NO_MORE_BRACKETS):
            ALL_QUOTED = True
            for w in words:
               ALL_QUOTED = ALL_QUOTED and (w[0] in ['"',"'"])
            if (ALL_QUOTED):
               return ('array(%s)' % PY_CODE)
         #--------------------------------------------------
         # If there are no more brackets and EACH entry
         # starts with a letter (e.g. a, a12), then we
         # must be concatenating; either arrays or possibly
         # a combination of arrays and scalar variables.
         # Otherwise there would need to be extra brackets.
         #--------------------------------------------------
         # If any of the variables is a scalar then the
         # call to concatenate() will produce a ValueError
         # and user will need to enclose that variable with
         # a square bracket.  Issue warning about this.
         #--------------------------------------------------
         if (NO_MORE_BRACKETS):
            ALL_ALPHA = True
            for w in words:
               ALL_ALPHA = ALL_ALPHA and (w[0].isalpha())
            if (ALL_ALPHA):
               print 'Warning: Make sure all args to concatenate() are arrays.'
               PY_CODE2 = '(' + PY_CODE[1:-1] + ')'
               return ('concatenate(%s)' % PY_CODE2)
         #--------------------------------------------------
         # If there are no more brackets and EACH entry
         # starts with either a letter or a digit, then we
         # must be concatenating; either arrays or possibly
         # a combination of arrays and scalar variables.
         # Otherwise there would need to be extra brackets.
         # But we must enclose each scalar in brackets.
         #--------------------------------------------------
         if (NO_MORE_BRACKETS):
            ALL_ALNUM = True
            for w in words:
               ALL_ALNUM = ALL_ALNUM and (w[0].isalnum())
            if (ALL_ALNUM):
               EXPR = ''
               for w in words:
                  if (w[0].isdigit()):
                     EXPR += '[' + w + '],'
                  else:
                     EXPR += w + ','
               EXPR = EXPR[0:-1]  # (remove last comma)
               print 'Warning: Make sure all args to concatenate() are arrays.'
               return ('concatenate((%s))' % EXPR)
         #----------------------------------------------------
         # NB!  This block processes all remaining cases.
         #----------------------------------------------------         
         # If  every occurrence of "]," is followed by "[",
         # and every occurrence of ",[" is preceded by "]",
         # then we must be creating an array.  Otherwise,
         # we must be doing a concatenation.  If we are
         # concatenating, add brackets around scalar numbers.
         #----------------------------------------------------
         # Note that the following doesn't work:
         #    a = concatenate(([1,2,3], 4))
         # Instead, we need to do this:
         #    a = concatenate(([1,2,3], [4])
         # or this:
         #    a = concatenate(( array([1,2,3]), array([4]) ))
         #----------------------------------------------------
         EXPR  = ''
         IS_ARRAY  = True
         ADD_RIGHT = False
         ADD_LEFT  = False
         c1 = ''
         c2 = ''
         for c in str1:
            if ((c1 + c2) == "],"):
               if (c != "["):
                  IS_ARRAY = False
                  if (c.isdigit()):
                     # Insert a left bracket
                     EXPR += "["
                     ADD_RIGHT = True  # (need matching)
            elif ((c2 + c) == ",["):
               if (c1 != "]"):
                  IS_ARRAY = False
                  if (c1.isdigit()):
                     # Insert a right bracket
                     EXPR = EXPR[:-1] + ("]" + c2)
                     ADD_LEFT = True   # (need matching)
            if (c == ',') and (ADD_RIGHT):
               EXPR += "]"
               ADD_RIGHT = False
            ## Don't seem to need anything else.
            ## if (something) and (ADD_LEFT):
            EXPR += c
            c2 = c
            if (len(EXPR) >= 2):
               c1 = EXPR[-2]
         if (ADD_RIGHT):  # (at end, and not added yet)
            EXPR += ']'
         if (ADD_LEFT):   # (at end, and not added yet)
            EXPR = '[' + EXPR
         if (IS_ARRAY):
            return ('array(%s)' % PY_CODE)
         else:
            print 'Warning: Make sure all args to concatenate() are arrays.'
            return ('concatenate((%s))' % EXPR)
       
         #--------------------------------------------------
         # The remaining possibilities are:  ******
         # and we can't distinguish between them.
         #--------------------------------------------------
##         print 'Warning: Unsure about square brackets. Assumed array().'
##         print '         ***** IDL expression =', IDL_EXPR, '*****'
##         return ('array(%s)' % PY_CODE)
      
         #------------------------------------------------
         # (SDP) This doesn't work in some places,
         # such as when POSITION=[0,0,1,1] in PLOT call.
         #------------------------------------------------
##         s = Node.pycode(self)
##         p = s.find("'")
##         if (p != -1):
##            return ('array(%s)' % s)
##         else:
##            cmd  = 'try:\n'
##            cmd += ('    I2PY_v = concatenate(%s)\n' % s)
##            cmd += 'except:\n'
##            cmd += ('    I2PY_v = array(%s)' % s)
##            return cmd

      #-----------------------------------------         
      # Need this for end of "pycode()" method
      #-----------------------------------------
      return Node.pycode(self)


#------------------------------------------------
# (SDP) PrimaryExpression class from I2PY 0.1.0
#------------------------------------------------
##class PrimaryExpression(Node):
##   def pycode(self):
##      if self.LBRACE:
##         # FIXME: implement this!
##         error.conversion_error("can't handle structures yet", self.lineno)
##         return ''
##      if self.LBRACKET:
##         return 'concatenate(%s)' % Node.pycode(self)
##      return Node.pycode(self)
   

class SubscriptList(Node):
   def pycode(self):
      if len(self) == 1:
         return pycode(self[0])
      return ','.join([pycode(self[2]), pycode(self[0])])


class Subscript(Node):
   def pycode(self):
      #------------------------------------------------------      
      # (SDP) Try to translate nested subscripts or indices
      #------------------------------------------------------
      EXPR = str(self)
      pos1 = EXPR.find('[')
      pos2 = EXPR.find(':')
      if (pos1 > 0) and (pos2 == -1):
          # print '***** str(self) =', EXPR
          
          indices1 = EXPR[:pos1]
          indices2 = EXPR[pos1+1:-1]
 
          # print '***** (indices1, indices2) =', indices1, indices2
          # print '-----------------------------------'

          #----------------------------------------------------
          # This approach is general, but need to remove
          # the outer square brackets, and don't have access?
          #----------------------------------------------------
          # EXPR = '.flat[' + indices2 + ']'
          
          #------------------------------------
          # This will only work for 2D arrays
          #----------------------------------------
          # Same idea would work for others if the
          # number of args equals number of dims.
          #----------------------------------------
##          print 'Warning: Assumed 2D array for nested index translation.'
##          arg1 = indices1 + '[0]' + '[' + indices2 + ']'
##          arg2 = indices1 + '[1]' + '[' + indices2 + ']'
##          comment = '  # (this assumes a 2D array)'
##          EXPR = '(' + arg1 + ',' + arg2 + ')' + comment
          
          return pycode(EXPR)
         
      #-------------------------------------------      
      if self.COLON:
         if not self.TIMES:
	    ulim = reduce_expression('(%s)+1' % pycode(self.expression[1]))
	    s = '%s:%s' % (pycode(self.expression[0]), ulim)
	    if len(self.expression) == 3:
	       s += ':%s' % pycode(self.expression[2])
	    return s
	 if len(self.expression) == 1:
	    return '%s:' % pycode(self.expression)
	 return '%s::%s' % (pycode(self.expression[0]),
	                    pycode(self.expression[1]))
      if self.TIMES:
         return ':'
      return pycode(self.expression)


class ExpressionList(_CommaSeparatedList):
   pass


class StructureBody(Node):
   def __str__(self):
      if self.IDENTIFIER:
	 s = str(self.IDENTIFIER)
	 if self.COMMA:
	    s += ', %s' % self.structure_field_list
         return s
      return Node.__str__(self)


class StructureFieldList(_CommaSeparatedList):
   pass


class StructureField(Node):
   def __str__(self):
      if self.INHERITS:
         return 'INHERITS %s' % self.IDENTIFIER
      return ''.join([ str(c) for c in self ])


