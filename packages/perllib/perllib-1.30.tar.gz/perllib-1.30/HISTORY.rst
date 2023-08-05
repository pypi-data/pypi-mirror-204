=======
History
=======

1.030 (2023-03-27)
------------------

* Issue s335: Replace os.getgrouplist() call in _stat.py with os.getgroups(), Issue s337: Fix issues in Time::HiRes on unix.  Issue s347: Converting a class object to a string should change '.' to '::' - fixed in _init_package, Issue s350: Handle dynamic require statement in eval - fix _import to handle '::' as '/', Issue s359: define get() in _ArrayHash to work with negative index, define get() in _add_tie_methods for tied arrays and also define proper __getitem__, __setitem__, and __delitem__ methods, define get() for File_stat class in _stat, fix _each to work on Array objects, allow _list_of_n to work on an itertools.chain object

1.029 (2023-03-03)
------------------

* Issue s311: Update _init_package to add a __bool__ method to all classes that returns True, Issue s324: Update _method_call to allow the methodname to be a function object, Issue s332: Implement promoting warnings to FATAL if WARNING is set to 2 - updates in _warn, _die, _flt, _num, _int

1.028 (2023-02-24)
------------------

* Issue s301: Add _assign_meta, _store_perl_meta, and _unassign_meta to support tie/untie of scalars.  Update _add_tie_methods to support tie scalar.  Implement use Env.  Issue s304: Add _add_tie_call.  Update _add_tie_methods to handle FIRSTKEY and NEXTKEY returning the list value from _each.

1.027 (2023-02-16)
------------------

* Issue s281: UNIVERSAL::isa(\*FH,'GLOB') should return 1.  Issue s295: `script.py` on windows will launch an editor if that's the associated program.  Issue s297: Set CHILD_ERROR properly in _run, _run_s, and _system.  Properly look up signal names in __members__ in _kill.  Issue s296: Create environment variables to set perllib.TRACKBACK, perllib.AUTODIE, perllib.TRACE_RUN, perllib.WARNING.  Implement in _init_package for main.  Issue s280: Don't try to set the __class__ attribute in _init_package on a non-class.  Issue 288: Implement new _warn.  Issue s292: Reimplement _die.  Implement CGI::Carp.

1.026 (2023-02-10)
------------------

* Fix _ref_scalar and _ref to change '.' to '::' when returning the __name__ attribute, then change _method_call to change '::' back to '.'.  Implement Time::localtime and Time::tm.  Retranslate Math::Complex with new Pythonizer.  Implement Time::HiRes.

1.025 (2023-02-05)
------------------

* Issue s269: Fix _import to handle the case where we haven't set our package yet.  Handle * for count in _pack.  Implement CGI, CGI::Cookie, CGI::Util.  Implement Encode via _encode, _decode, et.al. and Encode::Encoding, Encoding::MIME::Name.

1.024 (2023-01-30)
------------------

* Issue s260: Rewrite _caller and _callers.  Issue s244: In _store_perl_global, store a sub with both the escaped name and the unescaped name, and also call _ininit_package with is_class=True if the namespace is not a 'type'.  Add Class::Struct and Text::ParseWords packages.  Issue s261: Handle [:] in ArrayHash __setitem__ for slice.  Issue s266: _bless: Change "'" and '::' in classname to '.'

1.023 (2023-01-18)
------------------

* Issue s247: Add _exec and _execp.  Fix ArrayHash to defined __contains__.  Fix _add_tie_methods to handle a tie class that's both a hash and an array using a generator function.  Issue s253: fix _switch to handle objects that overload the smart match (~~) operator.  Issue s252: _read shouldn't raise an exception if given an int or None buffer.  Issue s244: add method_type argument to _store_perl_global.  Issue s259: Fix _caller and _callers to return the proper package (with some help from _init_package).

1.022 (2023-01-06)
------------------

* Issue s238: Update _cmp and _spaceship to work on objects with overloaded cmp and <=> operators - _cmp also now converts non-object to str internally, Added _overload_Method, _overload_Overloaded, _overloaded_StrVal, _subname.  Updated Math.Complex.py to set the new attributes we use to determine what's overloaded.  Add HTML::Entities.  Issue s243: Define UNIVERSAL as base class of all objects in _init_package and change the name of our _ArrayHashClass from NewCls to UNIVERSAL in ArrayHash.  Issue s244: update _store_perl_global to convert a callable to a MethodType if the method name is 'new' or 'make'.

1.021 (2022-12-28)
------------------

* Issue s223: Update the metaclass of our dynamically generated classes in _init_package to define a __str__ that returns the class name.  Update _ref_scalar to return '' if given a class (not a class instance), Issue s225: fix _import to actually work!, fix _tie_call if passed a string instead of self, Issue s231: Implement do EXPR in _import with a new keyword parameter, implement utf8:: functions, implement blessed, Issue s203: addl fix for _init_package to properly subclass MethodType subs, skip error in ArrayHash.extend if asked to extend a hash with an empty array as it is () in the source code, which is also used for an empty hash, Issue s236: _ref now returns '' for a class (not a class instance), Issue s237: add _logical_xor

1.020 (2022-12-20)
------------------

* Issue s18: Update _init_package to upgrade a SimpleNamespace to a type if we're called again and that is specified, also handle isa=... when is_class is False as inheritance still works in Perl without using bless, Issue s216: add _add_tie_methods, call it in _bless, Issue s218: change _num(object) to call _num_ if it's defined via use overload, change _init_package to define an 'is' comparison for classes and objects so == works as expected

1.019 (2022-12-10)
------------------

* Issue s209: Update _init_package to put all packages in the 'main' namespace and properly handle sub-namespaces, Issue scalar ref: add _ref_scalar for the ref function on various references held in scalars

1.018 (2022-12-05)
------------------

* Issue s184: Add _fetch_out_parameters for array/hash out parameters, fix _isa for Array or Hash type, Issue s198: add _list_of_at_least_n

1.017 (2022-12-04)
------------------

* Issue s185: Prepped _store_out_parameter to take None for arglist

1.016 (2022-11-30)
------------------

* Issue s184: Add _init_out_parameters, _store_out_parameter, and _fetch_out_parameter for supporting output parameters on functions and methods. Issue s183: Allow _perl_print to write to binary files to support binmode, fix autoflush with binmode

1.015 (2022-11-26)
------------------

* Issue s176: Add _fetch_perl_global and _store_perl_global, Issue s180: add _can for $obj->can('method'), fix error in _confess and _croak if TRACEBACK is false and the pythonizer -P option is used, then Die doesn't have a suppress_traceback keyword parameter, issue s177: Add _caller_s for scalar context caller function, have _read and _sysread already return a str, never bytes, issue s183: add _openhandle function

1.014 (2022-11-24)
------------------

* Issue s173: Fix File::Path to not reallocate the 'error' or 'result' arrays

1.013 (2022-11-14)
------------------

* Issue s152: have _import return 1 on success, issue s154: support tie, untie, tied, issue s166: update _open_dynamic, _dup to handle <&= and >&=, and _open to convert ints to string filenames, _system should not use capture_output

1.012 (2022-11-07)
------------------

* Issue s142: add Array.remove(item), issue s150: add _preprocess_arguments, _postprocess_arguments

1.011 (2022-11-03)
------------------

* Issue s135: Add _filter_map

1.010 (2022-11-03)
------------------

* (no library changes)

1.009 (2022-10-31)
------------------

* issue s128: Added _readlink, FindBin, issue s129: Added _switch

1.008 (2022-10-26)
------------------

* (no library changes)

1.007 (2022-10-24)
------------------

* (no library changes)

1.006 (2022-10-23)
------------------

* (no library changes)

1.005 (2022-10-21)
------------------

* issue s124: perllib functions should return 1 or '', not True/False

1.004 (2022-10-19)
------------------

* issue s122: IO encoding shouldn't default to UTF-8

1.003 (2022-10-17)
------------------

* issue s121: localtime, gmtime, and timelocal shouldn't raise exceptions

1.002 (2022-10-11)
------------------

* issue s119: Sparse extraction from array doesn't give proper results

1.001 (2022-10-01)
------------------

* First production version (no changes from 0.994)

0.994 (2022-09-29)
------------------

* issue s94: add _unlink, don't set OS_ERROR in _exc (used for eval errors)

0.993 (2022-09-26)
------------------

* (no library changes)

0.992 (2022-09-24)
------------------

* issue s105: newline at end of filename gets stripped by perl - fix in _open_

0.991 (2022-09-23)
------------------

* (no library changes)

0.990 (2022-09-22)
------------------

* (no library changes)

0.989 (2022-09-15)
------------------

* (no library changes)

0.988 (2022-09-15)
------------------

* (no library changes)

0.987 (2022-09-14)
------------------

* (no library changes)

0.986 (2022-09-09)
------------------

* (no library changes)

0.985 (2022-09-08)
------------------

* issue s99: If you have more formats than items, you get an error in python but not perl - fix in _format_

0.984 (2022-09-08)
------------------

* (no library changes)

0.983 (2022-09-04)
------------------

* (no library changes)

0.982 (2022-09-02)
------------------

* (no library changes)

0.981 (2022-08-02)
------------------

* (no library changes)

0.980 (2022-07-28)
------------------

* (no library changes)

0.979 (2022-07-02)
------------------

* issue s91 - open with a dynamic single argument that does not contain a mode returns None on error instead of a closed file.  Fix in _open_dynamic.

0.978 (2022-05-12)
------------------

* _system, _run, and _run_s are now able to run perl and python scripts under windows

0.977 (2022-04-29)
------------------

* (no library changes)

0.976 (2022-04-28)
------------------

* Add _strftime

0.975 (2022-04-28)
------------------

* (no library changes)

0.974 (2022-04-21)
------------------

* _num(blessed object) shouldn't return 0, _bless needs to treat the result as a dict, not an object.  Change method name for IO_File.open to have a trailing underscore to match the name after escape_keywords.  Fix typo "fd" in _IOFile_open to "fh".  perllib.close renamed to have a trailing underscore so that fh.close() doesn't cause infinite recursion.

0.973 (2022-04-16)
------------------

* (no library changes)

0.972 (2022-04-15)
------------------

* add _set_breakpoint

0.971 (2022-04-12)
------------------

* Add _split_s for split in a scalar context.  Add _splitdir, _splitpath, _curdir, and _updir from File::Spec.  Add _isa.  Add __contains__ in File_stat.  Add _chdir and _rmdir.

0.970 (2022-04-10)
------------------

* (no library changes)

0.969 (2022-04-05)
------------------

* Add _readdirs to handle readdir in list context, fix _each to handle arrays properly.  Fix _lstat so it actually works.

0.968 (2022-04-01)
------------------

* Add _utime, fix _stat and friends to work on filehandles and dirhandles.  Add _abspath for Cwd::abs_path.

0.967 (2022-03-31)
------------------

* (no library changes)

0.966 (2022-03-20)
------------------

* Convert variable to string in _substitute_global, _substitute_element, _translate_global, and _translate_element.  Change _ref to handle object checks and add _refs to handle ref with \ to a scalar, array, or hash - not perfect but it's normally correct.  Add _bless and enable _init_package to handle classes.  Fix _list_of_n and _make_list if you pass it a single Hash().  Add _flt for specific conversions to float, like in math functions.  Implement select via _select.  Implement kill via _kill.

0.965 (2022-03-14)
------------------

* Change Config.Config to Config.Config_h and all Dumper variables to include _v suffix to match new package var mappings in Pythonizer.  Add _map_int, _map_num, _map_str.  Fix _flatten to handle multiple levels. Change _longmess traceback to return '()' for args if they were changed to a list and all popped off instead of '[]'.  Handle OUTPUT_FIELD_SEPARATOR and OUTPUT_RECORD_SEPARATOR in _perl_print.  Fix charnames.viacode to handle 'U+' or '0x' prefix.

0.964 (2022-03-10)
------------------

* Fix _init_package for package with dotted name, don't raise exceptions in -C, -A, -M, fix Array __setitem__ with slice

0.963 (2022-03-09)
------------------

* Add _chop_global, _chomp_global, _chop_element, _chomp_element

0.962 (2022-03-09)
------------------

* Hot fix for _fileinput_next - errors on Python older than v3.10

0.961 (2022-03-02)
------------------

* Handle open layer pragmas, fix issue with translate and friends with squash option, add dclone, catfile, file_name_is_absolute, Dumper, don't raise exception on double close

0.960 (2022-02-28)
------------------

* Speed up ArrayHash and Num. Have add_element and subtract_element handle non-numeric elements, turn subprocess shell=False on windows unless the command contains cmd shell chars or is a cmd built-in, fixup open of /tmp/... on windows to use the windows tempdir, don't pass effective_ids=True on windows.  Have concat_element auto-convert everything to strings.

0.959 (2022-02-24)
------------------

* str(ArrayHash()) changed to give '' instead of [], add EVAL_ERROR global variable, have ArrayHash() + or += work on empty value

0.958 (2022-02-23)
------------------

* Don't give a close failed error on a pipe which got automatically closed, give empty result for keys(), values(), and items() on a fresh ArrayHash instead of AttributeError

0.957 (2022-02-22)
------------------

* Add list_to_hash function to process key/value pairs

0.956 (2022-02-21)
------------------

* Implement all options of translate (tr///)

0.955 (2022-02-19)
------------------

* Fix split: A zero-width match at the beginning of EXPR never produces an empty field, fix bootstrapping issues

0.954 (2022-02-17)
------------------

* Add -n: trace run, fix issue of scalar being initialized as an array

0.953 (2022-02-15)
------------------

* First release on PyPI.
