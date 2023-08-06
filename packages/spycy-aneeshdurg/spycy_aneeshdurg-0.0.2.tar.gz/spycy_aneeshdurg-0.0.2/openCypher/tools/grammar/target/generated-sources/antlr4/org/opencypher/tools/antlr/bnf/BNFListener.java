// Generated from org/opencypher/tools/antlr/bnf/BNF.g4 by ANTLR 4.7.2
package org.opencypher.tools.antlr.bnf;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link BNFParser}.
 */
public interface BNFListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link BNFParser#rulelist}.
	 * @param ctx the parse tree
	 */
	void enterRulelist(BNFParser.RulelistContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#rulelist}.
	 * @param ctx the parse tree
	 */
	void exitRulelist(BNFParser.RulelistContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#header}.
	 * @param ctx the parse tree
	 */
	void enterHeader(BNFParser.HeaderContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#header}.
	 * @param ctx the parse tree
	 */
	void exitHeader(BNFParser.HeaderContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#description}.
	 * @param ctx the parse tree
	 */
	void enterDescription(BNFParser.DescriptionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#description}.
	 * @param ctx the parse tree
	 */
	void exitDescription(BNFParser.DescriptionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#descriptionLine}.
	 * @param ctx the parse tree
	 */
	void enterDescriptionLine(BNFParser.DescriptionLineContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#descriptionLine}.
	 * @param ctx the parse tree
	 */
	void exitDescriptionLine(BNFParser.DescriptionLineContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#rule_}.
	 * @param ctx the parse tree
	 */
	void enterRule_(BNFParser.Rule_Context ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#rule_}.
	 * @param ctx the parse tree
	 */
	void exitRule_(BNFParser.Rule_Context ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#lhs}.
	 * @param ctx the parse tree
	 */
	void enterLhs(BNFParser.LhsContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#lhs}.
	 * @param ctx the parse tree
	 */
	void exitLhs(BNFParser.LhsContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#rhs}.
	 * @param ctx the parse tree
	 */
	void enterRhs(BNFParser.RhsContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#rhs}.
	 * @param ctx the parse tree
	 */
	void exitRhs(BNFParser.RhsContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#bnfsymbols}.
	 * @param ctx the parse tree
	 */
	void enterBnfsymbols(BNFParser.BnfsymbolsContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#bnfsymbols}.
	 * @param ctx the parse tree
	 */
	void exitBnfsymbols(BNFParser.BnfsymbolsContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#alternatives}.
	 * @param ctx the parse tree
	 */
	void enterAlternatives(BNFParser.AlternativesContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#alternatives}.
	 * @param ctx the parse tree
	 */
	void exitAlternatives(BNFParser.AlternativesContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#alternative}.
	 * @param ctx the parse tree
	 */
	void enterAlternative(BNFParser.AlternativeContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#alternative}.
	 * @param ctx the parse tree
	 */
	void exitAlternative(BNFParser.AlternativeContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#element}.
	 * @param ctx the parse tree
	 */
	void enterElement(BNFParser.ElementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#element}.
	 * @param ctx the parse tree
	 */
	void exitElement(BNFParser.ElementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#optionalitem}.
	 * @param ctx the parse tree
	 */
	void enterOptionalitem(BNFParser.OptionalitemContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#optionalitem}.
	 * @param ctx the parse tree
	 */
	void exitOptionalitem(BNFParser.OptionalitemContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#requireditem}.
	 * @param ctx the parse tree
	 */
	void enterRequireditem(BNFParser.RequireditemContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#requireditem}.
	 * @param ctx the parse tree
	 */
	void exitRequireditem(BNFParser.RequireditemContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#text}.
	 * @param ctx the parse tree
	 */
	void enterText(BNFParser.TextContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#text}.
	 * @param ctx the parse tree
	 */
	void exitText(BNFParser.TextContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#id}.
	 * @param ctx the parse tree
	 */
	void enterId(BNFParser.IdContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#id}.
	 * @param ctx the parse tree
	 */
	void exitId(BNFParser.IdContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#characterset}.
	 * @param ctx the parse tree
	 */
	void enterCharacterset(BNFParser.CharactersetContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#characterset}.
	 * @param ctx the parse tree
	 */
	void exitCharacterset(BNFParser.CharactersetContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#normaltext}.
	 * @param ctx the parse tree
	 */
	void enterNormaltext(BNFParser.NormaltextContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#normaltext}.
	 * @param ctx the parse tree
	 */
	void exitNormaltext(BNFParser.NormaltextContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#namedcharacterset}.
	 * @param ctx the parse tree
	 */
	void enterNamedcharacterset(BNFParser.NamedcharactersetContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#namedcharacterset}.
	 * @param ctx the parse tree
	 */
	void exitNamedcharacterset(BNFParser.NamedcharactersetContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#exclusioncharacterset}.
	 * @param ctx the parse tree
	 */
	void enterExclusioncharacterset(BNFParser.ExclusioncharactersetContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#exclusioncharacterset}.
	 * @param ctx the parse tree
	 */
	void exitExclusioncharacterset(BNFParser.ExclusioncharactersetContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#listcharacterset}.
	 * @param ctx the parse tree
	 */
	void enterListcharacterset(BNFParser.ListcharactersetContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#listcharacterset}.
	 * @param ctx the parse tree
	 */
	void exitListcharacterset(BNFParser.ListcharactersetContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#ruleref}.
	 * @param ctx the parse tree
	 */
	void enterRuleref(BNFParser.RulerefContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#ruleref}.
	 * @param ctx the parse tree
	 */
	void exitRuleref(BNFParser.RulerefContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#ruleid}.
	 * @param ctx the parse tree
	 */
	void enterRuleid(BNFParser.RuleidContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#ruleid}.
	 * @param ctx the parse tree
	 */
	void exitRuleid(BNFParser.RuleidContext ctx);
	/**
	 * Enter a parse tree produced by {@link BNFParser#bnfsymbol}.
	 * @param ctx the parse tree
	 */
	void enterBnfsymbol(BNFParser.BnfsymbolContext ctx);
	/**
	 * Exit a parse tree produced by {@link BNFParser#bnfsymbol}.
	 * @param ctx the parse tree
	 */
	void exitBnfsymbol(BNFParser.BnfsymbolContext ctx);
}