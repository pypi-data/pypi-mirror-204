// Generated from org/opencypher/tools/antlr/bnf/BNF.g4 by ANTLR 4.7.2
package org.opencypher.tools.antlr.bnf;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class BNFParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.7.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, ASSIGN=2, LBRACE=3, RBRACE=4, LEND=5, REND=6, BAR=7, GT=8, LT=9, 
		ELLIPSIS=10, DOUBLE_EXCLAM=11, DOLLAR=12, ID=13, NORMAL_TEXT=14, SINGLE_LINE_COMMENT=15, 
		INTEGER_LITERAL=16, CHARACTER_LITERAL=17, UNICODE_LITERAL=18, WS=19;
	public static final int
		RULE_rulelist = 0, RULE_header = 1, RULE_description = 2, RULE_descriptionLine = 3, 
		RULE_rule_ = 4, RULE_lhs = 5, RULE_rhs = 6, RULE_bnfsymbols = 7, RULE_alternatives = 8, 
		RULE_alternative = 9, RULE_element = 10, RULE_optionalitem = 11, RULE_requireditem = 12, 
		RULE_text = 13, RULE_id = 14, RULE_characterset = 15, RULE_normaltext = 16, 
		RULE_namedcharacterset = 17, RULE_exclusioncharacterset = 18, RULE_listcharacterset = 19, 
		RULE_ruleref = 20, RULE_ruleid = 21, RULE_bnfsymbol = 22;
	private static String[] makeRuleNames() {
		return new String[] {
			"rulelist", "header", "description", "descriptionLine", "rule_", "lhs", 
			"rhs", "bnfsymbols", "alternatives", "alternative", "element", "optionalitem", 
			"requireditem", "text", "id", "characterset", "normaltext", "namedcharacterset", 
			"exclusioncharacterset", "listcharacterset", "ruleref", "ruleid", "bnfsymbol"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'~'", "'::='", "'}'", "'{'", "']'", "'['", "'|'", "'>'", "'<'", 
			"'...'", "'!!'", "'$'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, "ASSIGN", "LBRACE", "RBRACE", "LEND", "REND", "BAR", "GT", 
			"LT", "ELLIPSIS", "DOUBLE_EXCLAM", "DOLLAR", "ID", "NORMAL_TEXT", "SINGLE_LINE_COMMENT", 
			"INTEGER_LITERAL", "CHARACTER_LITERAL", "UNICODE_LITERAL", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "BNF.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public BNFParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class RulelistContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(BNFParser.EOF, 0); }
		public HeaderContext header() {
			return getRuleContext(HeaderContext.class,0);
		}
		public List<Rule_Context> rule_() {
			return getRuleContexts(Rule_Context.class);
		}
		public Rule_Context rule_(int i) {
			return getRuleContext(Rule_Context.class,i);
		}
		public RulelistContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rulelist; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterRulelist(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitRulelist(this);
		}
	}

	public final RulelistContext rulelist() throws RecognitionException {
		RulelistContext _localctx = new RulelistContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_rulelist);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(47);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				{
				setState(46);
				header();
				}
				break;
			}
			setState(52);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==LT || _la==NORMAL_TEXT) {
				{
				{
				setState(49);
				rule_();
				}
				}
				setState(54);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(55);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class HeaderContext extends ParserRuleContext {
		public DescriptionContext description() {
			return getRuleContext(DescriptionContext.class,0);
		}
		public HeaderContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_header; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterHeader(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitHeader(this);
		}
	}

	public final HeaderContext header() throws RecognitionException {
		HeaderContext _localctx = new HeaderContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_header);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(57);
			description();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class DescriptionContext extends ParserRuleContext {
		public List<DescriptionLineContext> descriptionLine() {
			return getRuleContexts(DescriptionLineContext.class);
		}
		public DescriptionLineContext descriptionLine(int i) {
			return getRuleContext(DescriptionLineContext.class,i);
		}
		public DescriptionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_description; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterDescription(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitDescription(this);
		}
	}

	public final DescriptionContext description() throws RecognitionException {
		DescriptionContext _localctx = new DescriptionContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_description);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(60); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					{
					setState(59);
					descriptionLine();
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(62); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class DescriptionLineContext extends ParserRuleContext {
		public TerminalNode NORMAL_TEXT() { return getToken(BNFParser.NORMAL_TEXT, 0); }
		public DescriptionLineContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_descriptionLine; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterDescriptionLine(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitDescriptionLine(this);
		}
	}

	public final DescriptionLineContext descriptionLine() throws RecognitionException {
		DescriptionLineContext _localctx = new DescriptionLineContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_descriptionLine);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(64);
			match(NORMAL_TEXT);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rule_Context extends ParserRuleContext {
		public LhsContext lhs() {
			return getRuleContext(LhsContext.class,0);
		}
		public TerminalNode ASSIGN() { return getToken(BNFParser.ASSIGN, 0); }
		public RhsContext rhs() {
			return getRuleContext(RhsContext.class,0);
		}
		public DescriptionContext description() {
			return getRuleContext(DescriptionContext.class,0);
		}
		public Rule_Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rule_; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterRule_(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitRule_(this);
		}
	}

	public final Rule_Context rule_() throws RecognitionException {
		Rule_Context _localctx = new Rule_Context(_ctx, getState());
		enterRule(_localctx, 8, RULE_rule_);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(67);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==NORMAL_TEXT) {
				{
				setState(66);
				description();
				}
			}

			setState(69);
			lhs();
			setState(70);
			match(ASSIGN);
			setState(71);
			rhs();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LhsContext extends ParserRuleContext {
		public TerminalNode LT() { return getToken(BNFParser.LT, 0); }
		public RuleidContext ruleid() {
			return getRuleContext(RuleidContext.class,0);
		}
		public TerminalNode GT() { return getToken(BNFParser.GT, 0); }
		public LhsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_lhs; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterLhs(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitLhs(this);
		}
	}

	public final LhsContext lhs() throws RecognitionException {
		LhsContext _localctx = new LhsContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_lhs);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(73);
			match(LT);
			setState(74);
			ruleid();
			setState(75);
			match(GT);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class RhsContext extends ParserRuleContext {
		public List<BnfsymbolsContext> bnfsymbols() {
			return getRuleContexts(BnfsymbolsContext.class);
		}
		public BnfsymbolsContext bnfsymbols(int i) {
			return getRuleContext(BnfsymbolsContext.class,i);
		}
		public AlternativesContext alternatives() {
			return getRuleContext(AlternativesContext.class,0);
		}
		public RhsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rhs; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterRhs(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitRhs(this);
		}
	}

	public final RhsContext rhs() throws RecognitionException {
		RhsContext _localctx = new RhsContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_rhs);
		try {
			int _alt;
			setState(83);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(78); 
				_errHandler.sync(this);
				_alt = 1;
				do {
					switch (_alt) {
					case 1:
						{
						{
						setState(77);
						bnfsymbols();
						}
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					setState(80); 
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
				} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(82);
				alternatives();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BnfsymbolsContext extends ParserRuleContext {
		public List<BnfsymbolContext> bnfsymbol() {
			return getRuleContexts(BnfsymbolContext.class);
		}
		public BnfsymbolContext bnfsymbol(int i) {
			return getRuleContext(BnfsymbolContext.class,i);
		}
		public BnfsymbolsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bnfsymbols; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterBnfsymbols(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitBnfsymbols(this);
		}
	}

	public final BnfsymbolsContext bnfsymbols() throws RecognitionException {
		BnfsymbolsContext _localctx = new BnfsymbolsContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_bnfsymbols);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(86); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					{
					setState(85);
					bnfsymbol();
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(88); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,6,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AlternativesContext extends ParserRuleContext {
		public List<AlternativeContext> alternative() {
			return getRuleContexts(AlternativeContext.class);
		}
		public AlternativeContext alternative(int i) {
			return getRuleContext(AlternativeContext.class,i);
		}
		public List<TerminalNode> BAR() { return getTokens(BNFParser.BAR); }
		public TerminalNode BAR(int i) {
			return getToken(BNFParser.BAR, i);
		}
		public AlternativesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_alternatives; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterAlternatives(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitAlternatives(this);
		}
	}

	public final AlternativesContext alternatives() throws RecognitionException {
		AlternativesContext _localctx = new AlternativesContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_alternatives);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(90);
			alternative();
			setState(95);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==BAR) {
				{
				{
				setState(91);
				match(BAR);
				setState(92);
				alternative();
				}
				}
				setState(97);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AlternativeContext extends ParserRuleContext {
		public List<ElementContext> element() {
			return getRuleContexts(ElementContext.class);
		}
		public ElementContext element(int i) {
			return getRuleContext(ElementContext.class,i);
		}
		public AlternativeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_alternative; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterAlternative(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitAlternative(this);
		}
	}

	public final AlternativeContext alternative() throws RecognitionException {
		AlternativeContext _localctx = new AlternativeContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_alternative);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(101);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,8,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(98);
					element();
					}
					} 
				}
				setState(103);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,8,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ElementContext extends ParserRuleContext {
		public OptionalitemContext optionalitem() {
			return getRuleContext(OptionalitemContext.class,0);
		}
		public RequireditemContext requireditem() {
			return getRuleContext(RequireditemContext.class,0);
		}
		public TextContext text() {
			return getRuleContext(TextContext.class,0);
		}
		public IdContext id() {
			return getRuleContext(IdContext.class,0);
		}
		public CharactersetContext characterset() {
			return getRuleContext(CharactersetContext.class,0);
		}
		public NormaltextContext normaltext() {
			return getRuleContext(NormaltextContext.class,0);
		}
		public ElementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_element; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterElement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitElement(this);
		}
	}

	public final ElementContext element() throws RecognitionException {
		ElementContext _localctx = new ElementContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_element);
		try {
			setState(110);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case REND:
				enterOuterAlt(_localctx, 1);
				{
				setState(104);
				optionalitem();
				}
				break;
			case RBRACE:
				enterOuterAlt(_localctx, 2);
				{
				setState(105);
				requireditem();
				}
				break;
			case ID:
			case INTEGER_LITERAL:
			case CHARACTER_LITERAL:
			case UNICODE_LITERAL:
				enterOuterAlt(_localctx, 3);
				{
				setState(106);
				text();
				}
				break;
			case LT:
				enterOuterAlt(_localctx, 4);
				{
				setState(107);
				id();
				}
				break;
			case DOLLAR:
				enterOuterAlt(_localctx, 5);
				{
				setState(108);
				characterset();
				}
				break;
			case NORMAL_TEXT:
				enterOuterAlt(_localctx, 6);
				{
				setState(109);
				normaltext();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class OptionalitemContext extends ParserRuleContext {
		public TerminalNode REND() { return getToken(BNFParser.REND, 0); }
		public AlternativesContext alternatives() {
			return getRuleContext(AlternativesContext.class,0);
		}
		public TerminalNode LEND() { return getToken(BNFParser.LEND, 0); }
		public TerminalNode ELLIPSIS() { return getToken(BNFParser.ELLIPSIS, 0); }
		public OptionalitemContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_optionalitem; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterOptionalitem(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitOptionalitem(this);
		}
	}

	public final OptionalitemContext optionalitem() throws RecognitionException {
		OptionalitemContext _localctx = new OptionalitemContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_optionalitem);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(112);
			match(REND);
			setState(113);
			alternatives();
			setState(114);
			match(LEND);
			setState(116);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELLIPSIS) {
				{
				setState(115);
				match(ELLIPSIS);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class RequireditemContext extends ParserRuleContext {
		public TerminalNode RBRACE() { return getToken(BNFParser.RBRACE, 0); }
		public AlternativesContext alternatives() {
			return getRuleContext(AlternativesContext.class,0);
		}
		public TerminalNode LBRACE() { return getToken(BNFParser.LBRACE, 0); }
		public TerminalNode ELLIPSIS() { return getToken(BNFParser.ELLIPSIS, 0); }
		public RequireditemContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_requireditem; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterRequireditem(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitRequireditem(this);
		}
	}

	public final RequireditemContext requireditem() throws RecognitionException {
		RequireditemContext _localctx = new RequireditemContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_requireditem);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(118);
			match(RBRACE);
			setState(119);
			alternatives();
			setState(120);
			match(LBRACE);
			setState(122);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELLIPSIS) {
				{
				setState(121);
				match(ELLIPSIS);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class TextContext extends ParserRuleContext {
		public TerminalNode UNICODE_LITERAL() { return getToken(BNFParser.UNICODE_LITERAL, 0); }
		public TerminalNode ID() { return getToken(BNFParser.ID, 0); }
		public TerminalNode CHARACTER_LITERAL() { return getToken(BNFParser.CHARACTER_LITERAL, 0); }
		public TerminalNode INTEGER_LITERAL() { return getToken(BNFParser.INTEGER_LITERAL, 0); }
		public TextContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_text; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterText(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitText(this);
		}
	}

	public final TextContext text() throws RecognitionException {
		TextContext _localctx = new TextContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_text);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(124);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << ID) | (1L << INTEGER_LITERAL) | (1L << CHARACTER_LITERAL) | (1L << UNICODE_LITERAL))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class IdContext extends ParserRuleContext {
		public TerminalNode LT() { return getToken(BNFParser.LT, 0); }
		public RulerefContext ruleref() {
			return getRuleContext(RulerefContext.class,0);
		}
		public TerminalNode GT() { return getToken(BNFParser.GT, 0); }
		public TerminalNode ELLIPSIS() { return getToken(BNFParser.ELLIPSIS, 0); }
		public IdContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_id; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterId(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitId(this);
		}
	}

	public final IdContext id() throws RecognitionException {
		IdContext _localctx = new IdContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_id);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(126);
			match(LT);
			setState(127);
			ruleref();
			setState(128);
			match(GT);
			setState(130);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELLIPSIS) {
				{
				setState(129);
				match(ELLIPSIS);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class CharactersetContext extends ParserRuleContext {
		public List<TerminalNode> DOLLAR() { return getTokens(BNFParser.DOLLAR); }
		public TerminalNode DOLLAR(int i) {
			return getToken(BNFParser.DOLLAR, i);
		}
		public NamedcharactersetContext namedcharacterset() {
			return getRuleContext(NamedcharactersetContext.class,0);
		}
		public ExclusioncharactersetContext exclusioncharacterset() {
			return getRuleContext(ExclusioncharactersetContext.class,0);
		}
		public ListcharactersetContext listcharacterset() {
			return getRuleContext(ListcharactersetContext.class,0);
		}
		public CharactersetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_characterset; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterCharacterset(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitCharacterset(this);
		}
	}

	public final CharactersetContext characterset() throws RecognitionException {
		CharactersetContext _localctx = new CharactersetContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_characterset);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(132);
			match(DOLLAR);
			setState(136);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ID:
				{
				setState(133);
				namedcharacterset();
				}
				break;
			case T__0:
				{
				setState(134);
				exclusioncharacterset();
				}
				break;
			case REND:
				{
				setState(135);
				listcharacterset();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			setState(138);
			match(DOLLAR);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class NormaltextContext extends ParserRuleContext {
		public TerminalNode NORMAL_TEXT() { return getToken(BNFParser.NORMAL_TEXT, 0); }
		public NormaltextContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_normaltext; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterNormaltext(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitNormaltext(this);
		}
	}

	public final NormaltextContext normaltext() throws RecognitionException {
		NormaltextContext _localctx = new NormaltextContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_normaltext);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(140);
			match(NORMAL_TEXT);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class NamedcharactersetContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(BNFParser.ID, 0); }
		public NamedcharactersetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namedcharacterset; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterNamedcharacterset(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitNamedcharacterset(this);
		}
	}

	public final NamedcharactersetContext namedcharacterset() throws RecognitionException {
		NamedcharactersetContext _localctx = new NamedcharactersetContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_namedcharacterset);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(142);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ExclusioncharactersetContext extends ParserRuleContext {
		public ListcharactersetContext listcharacterset() {
			return getRuleContext(ListcharactersetContext.class,0);
		}
		public ExclusioncharactersetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_exclusioncharacterset; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterExclusioncharacterset(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitExclusioncharacterset(this);
		}
	}

	public final ExclusioncharactersetContext exclusioncharacterset() throws RecognitionException {
		ExclusioncharactersetContext _localctx = new ExclusioncharactersetContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_exclusioncharacterset);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(144);
			match(T__0);
			setState(145);
			listcharacterset();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ListcharactersetContext extends ParserRuleContext {
		public TerminalNode REND() { return getToken(BNFParser.REND, 0); }
		public TerminalNode LEND() { return getToken(BNFParser.LEND, 0); }
		public List<TextContext> text() {
			return getRuleContexts(TextContext.class);
		}
		public TextContext text(int i) {
			return getRuleContext(TextContext.class,i);
		}
		public ListcharactersetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listcharacterset; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterListcharacterset(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitListcharacterset(this);
		}
	}

	public final ListcharactersetContext listcharacterset() throws RecognitionException {
		ListcharactersetContext _localctx = new ListcharactersetContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_listcharacterset);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(147);
			match(REND);
			setState(149); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(148);
				text();
				}
				}
				setState(151); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << ID) | (1L << INTEGER_LITERAL) | (1L << CHARACTER_LITERAL) | (1L << UNICODE_LITERAL))) != 0) );
			setState(153);
			match(LEND);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class RulerefContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(BNFParser.ID, 0); }
		public RulerefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleref; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterRuleref(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitRuleref(this);
		}
	}

	public final RulerefContext ruleref() throws RecognitionException {
		RulerefContext _localctx = new RulerefContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_ruleref);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(155);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class RuleidContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(BNFParser.ID, 0); }
		public RuleidContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleid; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterRuleid(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitRuleid(this);
		}
	}

	public final RuleidContext ruleid() throws RecognitionException {
		RuleidContext _localctx = new RuleidContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_ruleid);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(157);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BnfsymbolContext extends ParserRuleContext {
		public TerminalNode ASSIGN() { return getToken(BNFParser.ASSIGN, 0); }
		public TerminalNode LBRACE() { return getToken(BNFParser.LBRACE, 0); }
		public TerminalNode RBRACE() { return getToken(BNFParser.RBRACE, 0); }
		public TerminalNode LEND() { return getToken(BNFParser.LEND, 0); }
		public TerminalNode REND() { return getToken(BNFParser.REND, 0); }
		public TerminalNode BAR() { return getToken(BNFParser.BAR, 0); }
		public TerminalNode GT() { return getToken(BNFParser.GT, 0); }
		public TerminalNode LT() { return getToken(BNFParser.LT, 0); }
		public TerminalNode ELLIPSIS() { return getToken(BNFParser.ELLIPSIS, 0); }
		public TerminalNode DOUBLE_EXCLAM() { return getToken(BNFParser.DOUBLE_EXCLAM, 0); }
		public TerminalNode DOLLAR() { return getToken(BNFParser.DOLLAR, 0); }
		public BnfsymbolContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bnfsymbol; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).enterBnfsymbol(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BNFListener ) ((BNFListener)listener).exitBnfsymbol(this);
		}
	}

	public final BnfsymbolContext bnfsymbol() throws RecognitionException {
		BnfsymbolContext _localctx = new BnfsymbolContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_bnfsymbol);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(159);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << ASSIGN) | (1L << LBRACE) | (1L << RBRACE) | (1L << LEND) | (1L << REND) | (1L << BAR) | (1L << GT) | (1L << LT) | (1L << ELLIPSIS) | (1L << DOUBLE_EXCLAM) | (1L << DOLLAR))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\25\u00a4\4\2\t\2"+
		"\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\3\2\5\2\62"+
		"\n\2\3\2\7\2\65\n\2\f\2\16\28\13\2\3\2\3\2\3\3\3\3\3\4\6\4?\n\4\r\4\16"+
		"\4@\3\5\3\5\3\6\5\6F\n\6\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\b\6\bQ\n\b"+
		"\r\b\16\bR\3\b\5\bV\n\b\3\t\6\tY\n\t\r\t\16\tZ\3\n\3\n\3\n\7\n`\n\n\f"+
		"\n\16\nc\13\n\3\13\7\13f\n\13\f\13\16\13i\13\13\3\f\3\f\3\f\3\f\3\f\3"+
		"\f\5\fq\n\f\3\r\3\r\3\r\3\r\5\rw\n\r\3\16\3\16\3\16\3\16\5\16}\n\16\3"+
		"\17\3\17\3\20\3\20\3\20\3\20\5\20\u0085\n\20\3\21\3\21\3\21\3\21\5\21"+
		"\u008b\n\21\3\21\3\21\3\22\3\22\3\23\3\23\3\24\3\24\3\24\3\25\3\25\6\25"+
		"\u0098\n\25\r\25\16\25\u0099\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3"+
		"\30\2\2\31\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\2\4\4\2\17"+
		"\17\22\24\3\2\4\16\2\u00a0\2\61\3\2\2\2\4;\3\2\2\2\6>\3\2\2\2\bB\3\2\2"+
		"\2\nE\3\2\2\2\fK\3\2\2\2\16U\3\2\2\2\20X\3\2\2\2\22\\\3\2\2\2\24g\3\2"+
		"\2\2\26p\3\2\2\2\30r\3\2\2\2\32x\3\2\2\2\34~\3\2\2\2\36\u0080\3\2\2\2"+
		" \u0086\3\2\2\2\"\u008e\3\2\2\2$\u0090\3\2\2\2&\u0092\3\2\2\2(\u0095\3"+
		"\2\2\2*\u009d\3\2\2\2,\u009f\3\2\2\2.\u00a1\3\2\2\2\60\62\5\4\3\2\61\60"+
		"\3\2\2\2\61\62\3\2\2\2\62\66\3\2\2\2\63\65\5\n\6\2\64\63\3\2\2\2\658\3"+
		"\2\2\2\66\64\3\2\2\2\66\67\3\2\2\2\679\3\2\2\28\66\3\2\2\29:\7\2\2\3:"+
		"\3\3\2\2\2;<\5\6\4\2<\5\3\2\2\2=?\5\b\5\2>=\3\2\2\2?@\3\2\2\2@>\3\2\2"+
		"\2@A\3\2\2\2A\7\3\2\2\2BC\7\20\2\2C\t\3\2\2\2DF\5\6\4\2ED\3\2\2\2EF\3"+
		"\2\2\2FG\3\2\2\2GH\5\f\7\2HI\7\4\2\2IJ\5\16\b\2J\13\3\2\2\2KL\7\13\2\2"+
		"LM\5,\27\2MN\7\n\2\2N\r\3\2\2\2OQ\5\20\t\2PO\3\2\2\2QR\3\2\2\2RP\3\2\2"+
		"\2RS\3\2\2\2SV\3\2\2\2TV\5\22\n\2UP\3\2\2\2UT\3\2\2\2V\17\3\2\2\2WY\5"+
		".\30\2XW\3\2\2\2YZ\3\2\2\2ZX\3\2\2\2Z[\3\2\2\2[\21\3\2\2\2\\a\5\24\13"+
		"\2]^\7\t\2\2^`\5\24\13\2_]\3\2\2\2`c\3\2\2\2a_\3\2\2\2ab\3\2\2\2b\23\3"+
		"\2\2\2ca\3\2\2\2df\5\26\f\2ed\3\2\2\2fi\3\2\2\2ge\3\2\2\2gh\3\2\2\2h\25"+
		"\3\2\2\2ig\3\2\2\2jq\5\30\r\2kq\5\32\16\2lq\5\34\17\2mq\5\36\20\2nq\5"+
		" \21\2oq\5\"\22\2pj\3\2\2\2pk\3\2\2\2pl\3\2\2\2pm\3\2\2\2pn\3\2\2\2po"+
		"\3\2\2\2q\27\3\2\2\2rs\7\b\2\2st\5\22\n\2tv\7\7\2\2uw\7\f\2\2vu\3\2\2"+
		"\2vw\3\2\2\2w\31\3\2\2\2xy\7\6\2\2yz\5\22\n\2z|\7\5\2\2{}\7\f\2\2|{\3"+
		"\2\2\2|}\3\2\2\2}\33\3\2\2\2~\177\t\2\2\2\177\35\3\2\2\2\u0080\u0081\7"+
		"\13\2\2\u0081\u0082\5*\26\2\u0082\u0084\7\n\2\2\u0083\u0085\7\f\2\2\u0084"+
		"\u0083\3\2\2\2\u0084\u0085\3\2\2\2\u0085\37\3\2\2\2\u0086\u008a\7\16\2"+
		"\2\u0087\u008b\5$\23\2\u0088\u008b\5&\24\2\u0089\u008b\5(\25\2\u008a\u0087"+
		"\3\2\2\2\u008a\u0088\3\2\2\2\u008a\u0089\3\2\2\2\u008b\u008c\3\2\2\2\u008c"+
		"\u008d\7\16\2\2\u008d!\3\2\2\2\u008e\u008f\7\20\2\2\u008f#\3\2\2\2\u0090"+
		"\u0091\7\17\2\2\u0091%\3\2\2\2\u0092\u0093\7\3\2\2\u0093\u0094\5(\25\2"+
		"\u0094\'\3\2\2\2\u0095\u0097\7\b\2\2\u0096\u0098\5\34\17\2\u0097\u0096"+
		"\3\2\2\2\u0098\u0099\3\2\2\2\u0099\u0097\3\2\2\2\u0099\u009a\3\2\2\2\u009a"+
		"\u009b\3\2\2\2\u009b\u009c\7\7\2\2\u009c)\3\2\2\2\u009d\u009e\7\17\2\2"+
		"\u009e+\3\2\2\2\u009f\u00a0\7\17\2\2\u00a0-\3\2\2\2\u00a1\u00a2\t\3\2"+
		"\2\u00a2/\3\2\2\2\21\61\66@ERUZagpv|\u0084\u008a\u0099";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}