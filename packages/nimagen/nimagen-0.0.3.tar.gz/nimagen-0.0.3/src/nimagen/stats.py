"""
stats.py
Uses to perform mass univariate and everything related to it
"""
from typing import List, Union, Optional
from collections import defaultdict
from itertools import combinations
import statsmodels.api as sm
import statsmodels.formula.api as sfm
from statsmodels.stats.multitest import fdrcorrection
from scipy.stats import ttest_ind, zscore, f
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

from patsy import PatsyError

import tqdm
from statsmodels.multivariate.cancorr import CanCorr

from numpy.core._exceptions import UFuncTypeError

class MassUnivariate:
    
    @staticmethod
    def prepare_data(return_type='dict',**kwargs):
        """
        prepare the dependent and independent variables.

        Parameters
        ----------
        See mass_univariate
        
        Raises
        ------
        TypeError
            cat independentVar and cont independentVar needs to be list of strings, not list of list.

        Returns
        -------
        dependentvar and independentvar pd.DataFrames.

        """
        df = kwargs.get('df',None)
        cat_independentVar_cols = kwargs.get('cat_independentVar_cols',None)
        cont_independentVar_cols = kwargs.get('cont_independentVar_cols',None)
        dependentVar_cols = kwargs.get('dependentVar_cols',None)
        col_to_drop = kwargs.get('col_to_drop',None)
        
        
        cat_independentVar = defaultdict(list)
        cont_independentVar = defaultdict(list)
        dependentVar = defaultdict(list)
        
        ###############CATEGORICAL VARIABLES###############
        
        if isinstance(cat_independentVar_cols,(pd.DataFrame,pd.Series)):
            if isinstance(cat_independentVar_cols,pd.Series): # only 1 column
                cat_independentVar_cols = pd.DataFrame(cat_independentVar_cols)
            cat_independentVar.update(cat_independentVar_cols.to_dict(orient='list'))
        
        elif isinstance(cat_independentVar_cols, np.ndarray):
            # if array, check dimension, each column is treated as an independent variable
            if cat_independentVar_cols.ndim == 1:
                cat_independentVar_cols = cat_independentVar_cols.reshape(-1,1)
            for col in range(cat_independentVar_cols.shape[1]):
                cat_independentVar.update({f'Cat_{col}':cat_independentVar_cols[:,col]})   
        
        elif isinstance(cat_independentVar_cols,(list,str)):
            if all(isinstance(variable, str) for variable in cat_independentVar_cols) and isinstance(df, pd.DataFrame):
                # if it is string
                if isinstance(cat_independentVar_cols,str):
                    cat_independentVar_cols = [cat_independentVar_cols]
                cat_independentVar.update(df[cat_independentVar_cols].to_dict(orient='list'))
            else:
                raise TypeError('Check again input for categorical data, make sure it is list of strings, not list of lists of strings')
            
        ###############CONTINUOUS VARIABLES###############
        if isinstance(cont_independentVar_cols, (pd.DataFrame,pd.Series)):
            if isinstance(cont_independentVar_cols,pd.Series): # only 1 column
                cont_independentVar_cols = pd.DataFrame(cont_independentVar_cols)
            cont_independentVar.update(cont_independentVar_cols.to_dict(orient='list'))
        
        elif isinstance(cont_independentVar_cols, np.ndarray):
            # if array, check dimension, each column is treated as an independent variable
            if cont_independentVar_cols.ndim == 1:
                cont_independentVar_cols = cont_independentVar_cols.reshape(-1,1)
            for col in range(cont_independentVar_cols.shape[1]):
                cont_independentVar.update({f'Cont_{col}':cont_independentVar_cols[:,col]})
        
        elif isinstance(cont_independentVar_cols,(list,str)):
            if all(isinstance(variable, str) for variable in cont_independentVar_cols) and isinstance(df, pd.DataFrame):
                if isinstance(cont_independentVar_cols,str):
                    cont_independentVar_cols = [cont_independentVar_cols]
                cont_independentVar.update(df[cont_independentVar_cols].to_dict(orient='list'))
            else:
                raise TypeError('Check again input for continuous data, make sure it is list of strings, not list of lists of strings')
    
        
        ###############DEPENDENT VARIABLES###############
        if isinstance(dependentVar_cols, (pd.DataFrame,pd.Series)):
            if isinstance(dependentVar_cols,pd.Series): # only 1 column
                dependentVar_cols = pd.DataFrame(dependentVar_cols)
            dependentVar.update(dependentVar_cols.to_dict(orient='list'))
            
        elif isinstance(dependentVar_cols, np.ndarray):
            # if array, check dimension, each column is treated as an independent variable
            if dependentVar_cols.ndim == 1:
                dependentVar_cols = dependentVar_cols.reshape(-1,1)
            for col in range(dependentVar_cols.shape[1]):
                dependentVar.update({f'Dependent_Var_{col}':dependentVar_cols[:,col]})
        
        elif isinstance(dependentVar_cols,(list,str)):
            if all(isinstance(variable, str) for variable in dependentVar_cols) and isinstance(df, pd.DataFrame):
                if isinstance(dependentVar_cols,str):
                    dependentVar_cols = [dependentVar_cols]
                dependentVar.update(df[dependentVar_cols].to_dict(orient='list'))
                
            else:
                raise TypeError('Check again input for dependent data, \
                                make sure it is list of strings, not list of lists of strings')
        
        ##############REMOVE any variable#################
        if isinstance(col_to_drop,str):
            col_to_drop = [col_to_drop]
        if isinstance(col_to_drop,list):
            for col in col_to_drop:
                cat_independentVar.pop(col,None)
                cont_independentVar.pop(col,None)
                dependentVar.pop(col,None)
        
        if return_type=='dict':
            return cat_independentVar, cont_independentVar, dependentVar
        elif return_type=='dataframe':
            return pd.DataFrame(cat_independentVar), pd.DataFrame(cont_independentVar), pd.DataFrame(dependentVar)

    @staticmethod
    def print_lm_summary(model,return_ancova=False,**kwargs):
        typ=kwargs.get('typ',1)
        result = [None] * (len(model.params) + len(model.pvalues))
        result[::2] = model.params
        result[1::2] = model.pvalues
        if return_ancova:
            anova_table = sm.stats.anova_lm(model, typ=typ)
            anova_table = anova_table[['F','PR(>F)']][:-1].to_dict(orient='list') # the last row is residual no need
            anova_result = [None] * (len(anova_table['F'])+len(anova_table['PR(>F)']))
            anova_result[::2] = anova_table['F']
            anova_result[1::2] = anova_table['PR(>F)']
            result = result + anova_result
        return result
    

    @staticmethod
    def patsy_formula(dependent_key:str,
                      categorical_keys:List[str]=None,
                      continuous_keys:List[str]=None,
                      fit_intercept=True,
                      scaling:str='x',
                      formula:str=None):
        """Create patsy formula (i.e., R style formula to fit to ols)

        Args:
            dependent_key (str): The dependent key on the left side of the equation
            categorical_keys (List[str], optional): The list of categorical keys on the right side of the equation
            continuous_keys (List[str], optional): The list of continuous keys on the right side of the equation
            fit_intercept (bool, optional): Defaults to True.
            scaling (str, optional): Whether to perform standardize; can be {'x','y' or 'both'}. Defaults to 'x'.
            formula (str, optional): formula in R style. Defaults to None.

        Returns:
            formula: str formula in R style
        """
        def weird_symbols(key_list):
            if key_list is not None:
                if not isinstance(key_list,str):
                    return [f"Q('{k}')" if (' ' in k) or ('-' in k) or ('_' in k) else k for k in key_list]
                return f"Q('{key_list}')" if (' ' in key_list) else key_list
            
        if isinstance(formula,str):
            if '~' in formula:
                return formula
            else:
                right_side = formula
                
        else:
            categorical_keys = [] if weird_symbols(categorical_keys) is None else weird_symbols(categorical_keys)
            continuous_keys = [] if weird_symbols(continuous_keys) is None else weird_symbols(continuous_keys)
            right_side = '+'.join([f'C({k})' for k in categorical_keys] + 
                                  [f'standardize({k})' if scaling=='x' or scaling=='both' else k for k in continuous_keys])
            if not fit_intercept:
                right_side = right_side + ' -1'
                
        left_side = f'standardize({weird_symbols(dependent_key)})' if scaling=='y' or scaling=='both' else weird_symbols(dependent_key) 
        return '~'.join([left_side,right_side])
        
    @staticmethod
    def mass_univariate(df: Optional[pd.DataFrame] = None,
                        cat_independentVar_cols: Union[List[str],
                                                        np.ndarray,
                                                        pd.DataFrame,
                                                        pd.Series] = None,
                        cont_independentVar_cols: Union[List[str],
                                                        np.ndarray,
                                                        pd.DataFrame,
                                                        pd.Series] = None,
                        dependentVar_cols: Union[List[str],
                                                        np.ndarray,
                                                        pd.DataFrame,
                                                        pd.Series] = None,
                        formula: str = None,
                        fit_intercept=True,
                        scaling: str='x',
                        return_ancova=False,
                        col_to_drop : Optional[List[str]] = None,
                        additional_info=None,**kwargs) -> Union[sm.regression.linear_model.RegressionResultsWrapper, pd.DataFrame]:
        """[Returns the model and model summary
            Performs univariate test, implements statsmodel.api.OLS]

        Args:
            df (Optional[pd.DataFrame]): [pandas data frame, where each row is one observation]
            cat_independentVar_cols (Optional[Union[List[str], List[np.ndarray]]], optional): [list of categorical variables, such that they will be converted to dummies by pandas]. Defaults to None.
            cont_independentVar_cols (Optional[Union[List[str], List[np.ndarray]]], optional): [list of continuous variables, they will be appended to cat_independentVar_cols]. Defaults to None.
            dependentVar_cols (Optional[Union[List[str], List[np.ndarray]]], optional): [the dependent variable, the ]. Defaults to None.
            scaling [str]: Default = both. ('x','y','both','none') # if scaling both = essentially calculating correlation
            If none, we will not perform standard scaler, 'both' we will perform on both x (independent variable- feature) and y (dependent variable- target)
            col_to_drop [list[str]] = if we want to remove any column from the independent Variable before fitting the model.
            additional_info ([type], optional): [additional columns to be appended]. Defaults to None.

        Returns:
            Union[sm.regression.linear_model.RegressionResultsWrapper, pd.DataFrame]: [the statsmodel model and dataframe of the model summary, where cols are independent variables and const]
        """
        lm_summary = defaultdict(list)
        if isinstance(df,pd.DataFrame):
            df_dictionary = df.to_dict(orient='list')
        
        cat_independentVar,cont_independentVar,dependentVar = MassUnivariate.prepare_data(
            df=df,
            cat_independentVar_cols=cat_independentVar_cols,
            cont_independentVar_cols=cont_independentVar_cols,
            dependentVar_cols=dependentVar_cols,
            col_to_drop = col_to_drop
            )
        
        
        if isinstance(formula,str) and isinstance(df,pd.DataFrame):
            # if formula is provided, straightforward just plug and play.
            if '~' in formula: # ignore all other inputed variables
                last_model = sfm.ols(formula, data=df).fit()
                return last_model
            else: # providing only the independent variable, but not y
            #here we can have multiple y if needed
                df_dictionary.update(dependentVar)
                for feature in dependentVar.keys():
                    formula_temp= MassUnivariate.patsy_formula(feature,
                                                               formula=formula,
                                                               )
                    last_model = sfm.ols(formula_temp,data = df_dictionary).fit()
                    lm_summary[feature].extend(MassUnivariate.print_lm_summary(last_model,return_ancova=return_ancova,**kwargs))

        elif formula is None:
            for feature in dependentVar.keys():
                formula_temp = MassUnivariate.patsy_formula(feature,
                                                            cat_independentVar.keys(),
                                                            cont_independentVar.keys(),
                                                            fit_intercept=fit_intercept,
                                                            scaling=scaling)
                temp_dataset = dict()
                temp_dataset.update(cat_independentVar)
                temp_dataset.update(cont_independentVar)
                temp_dataset.update({feature:dependentVar[feature]})
                
                try:
                    last_model = sfm.ols(formula_temp,data=temp_dataset).fit()
                except PatsyError:
                    raise TypeError('You may be fitting standardize to a non-numeric value, change your scaling parameter')
                lm_summary[feature].extend(MassUnivariate.print_lm_summary(last_model,return_ancova=return_ancova,**kwargs))

        lm_summary = pd.DataFrame(lm_summary).T
        list1 = last_model.model.exog_names
        list2 = ['_coef', '_pval']
        lm_summary_columns = [i + n for i in list1 for n in list2]
        if return_ancova:
            list1 = last_model.model.data.design_info.term_names[1:] #first one is intercept not needed
            list2 = ['_F','_(PR>F)']
            lm_summary_columns = lm_summary_columns + [i + n for i in list1 for n in list2]
        lm_summary.columns = lm_summary_columns
        
        
        if additional_info:
            lm_summary['Additional_info'] = additional_info
            lm_summary.columns = [i for i in lm_summary.columns if 'Additional_info' not in i] + ['Additional_info']
        return last_model, lm_summary
    
    @staticmethod
    def remove_outliers(df:pd.DataFrame,
                        col:Union[str,List]=None,
                        threshold:float=None,
                        remove_schemes:str='any',
                        percentage_of_outlier:float=0.2,
                        subject_ID:list=None) -> pd.DataFrame:
        """[Remove outliers using the z-score (the same as using StandardScaler). The standard deviation]

        Args:
            df (pd.DataFrame): [Dataframe of interest]
            col (str or List, optional): [column of interest]. Defaults to None.
            threshold (float, optional): [the threshold of the z-score]. Defaults to None.
            subject_ID (list, optional): [Or gives me the list of subject IDs and remove by that way]. Defaults to None.

        Returns:
            pd.DataFrame: [New data frame without the outliers]
        """
        new_df = df.copy()
        idx_to_remove_by_col=[]
        idx_to_remove_by_ID=[]
        if col is not None:
            if not isinstance(col,list):
                col = [col]
            if remove_schemes == 'any': #remove observations that have outlier in any of the examined column
                idx_to_remove_by_col = new_df.loc[(np.abs(zscore(new_df[col]))>threshold).any(axis=1)].index.to_list()
            elif remove_schemes == 'all': #remove observations that have outlier in all of the examined column
                idx_to_remove_by_col = new_df.loc[(np.abs(zscore(new_df[col]))>threshold).all(axis=1)].index.to_list()
            elif remove_schemes == 'sum': # sum up the cols of interests and remove the outlier based on that sum
                idx_to_remove_by_col = new_df.loc[(np.abs(zscore(new_df[col].sum(axis=1)))>threshold)].index.to_list()
            elif remove_schemes == 'percentage': # remove observations that have more than x% of all features are outliers
                all_zscores = np.abs(zscore(new_df[col]))
                idx_to_remove_by_col = new_df.loc[(all_zscores>threshold).mean(axis=1)>=percentage_of_outlier].index.to_list()
        if subject_ID is not None:
            idx_to_remove_by_ID = (new_df.iloc[[idx for idx,i in enumerate(new_df.ID) if i in subject_ID]].index.to_list())
        idx_to_remove = idx_to_remove_by_col + idx_to_remove_by_ID
        idx_to_remove = list(set(idx_to_remove))
        new_df = new_df.drop(idx_to_remove).reset_index(drop = True)
        return new_df

    @staticmethod
    def adjust_covariates_with_lin_reg(df:pd.DataFrame=None,
                                       cat_independentVar_cols: Union[List[str],
                                                                      np.ndarray,
                                                                      pd.DataFrame,
                                                                      pd.Series] = None,
                                       cont_independentVar_cols: Union[List[str],
                                                                       np.ndarray,
                                                                       pd.DataFrame,
                                                                       pd.Series] = None,
                                       dependentVar_cols: Union[List[str],
                                                                np.ndarray,
                                                                pd.DataFrame,
                                                                pd.Series] = None,
                                      return_model_adjuster:bool=False,
                                       **massunivariatekwargs) -> pd.DataFrame:
        """
        Adjusting covariates by using linear regression

        Parameters
        ----------
        df : pd.DataFrame, optional
            The dataframe if providing strings as covariates. The default is None.
        cat_independentVar_cols : Union[List[str],np.ndarray,pd.DataFrame,pd.Series], optional
            The categorical variables. The default is None.
        cont_independentVar_cols : Union[List[str],np.ndarray,pd.DataFrame,pd.Series], optional
            The continuous variables. The default is None.
        dependentVar_cols : Union[List[str],np.ndarray,pd.DataFrame,pd.Series], optional
            The variables needed to be adjusted. The default is None.
        return_model_adjuster:bool
            Return a dictionary of linear models used to fit.
        *massunivariatekwargs : dict
            Anything from the MassUnivariate.mass_univariate function.

        Returns
        -------
        pd.DataFrame
            The dataframe of the adjusted variables, the columns will be the same as the one provided. The index will be the same as the df if provided.

        """
        adjusted_X = defaultdict(list)
        model_list = defaultdict(list)
        if isinstance(dependentVar_cols,(np.ndarray,pd.DataFrame,pd.Series)):
            if isinstance(dependentVar_cols,(pd.DataFrame,pd.Series)):
                if isinstance(dependentVar_cols,pd.Series):
                    dependentVar_cols = pd.DataFrame(dependentVar_cols)
                X = dependentVar_cols.values
            else:
                X = dependentVar_cols
            if X.ndim == 1:
                X = X.reshape(-1,1)
            for idx in range(X.shape[1]):
                model,_ = MassUnivariate.mass_univariate(
                    df = df,
                    cat_independentVar_cols=cat_independentVar_cols,
                    cont_independentVar_cols=cont_independentVar_cols,
                    dependentVar_cols=X[:,idx],**massunivariatekwargs
                    )
                if isinstance(dependentVar_cols, pd.DataFrame):
                    adjusted_X[dependentVar_cols.columns.tolist()[idx]] = model.resid.values
                else:
                    adjusted_X[idx] = model.resid.values
                if return_model_adjuster:
                    model_list[idx] = model
        if isinstance(dependentVar_cols,(list,str)):
            if isinstance(dependentVar_cols,str):
                dependentVar_cols = [dependentVar_cols]
            for idx,dependentVar_col in enumerate(dependentVar_cols):
                model,_ = MassUnivariate.mass_univariate(
                    df = df,
                    cat_independentVar_cols=cat_independentVar_cols,
                    cont_independentVar_cols=cont_independentVar_cols,
                    dependentVar_cols=dependentVar_col,
                    **massunivariatekwargs
                    )
                if isinstance(dependentVar_col,str):
                    adjusted_X[dependentVar_col] = model.resid.values
                else:
                    adjusted_X[idx] = model.resid.values
                if return_model_adjuster:
                    model_list[idx] = model
        adjusted_X = pd.DataFrame(adjusted_X)
        if df is not None:
            adjusted_X.index = df.index
        if return_model_adjuster:
            return adjusted_X, model_list
        return adjusted_X
        
    @classmethod
    def calculate_mass_univariate_across_multiple_thresholds(
            cls,
            df: pd.DataFrame,
            thresholds: List[str],
            threshold_prefix:str = 'PRS',
            cat_independentVar_cols: Optional[Union[List[str],
                                            List[np.ndarray]]] = None,
            cont_independentVar_cols: Optional[Union[List[str],
                                                    List[np.ndarray]]] = None,
            dependentVar_cols: Optional[Union[List[str],
                                            List[np.ndarray]]] = None,**kwargs) -> pd.DataFrame:
        """
        

        Parameters
        ----------
        df : pd.DataFrame
            the dataframe.
        thresholds : List[str]
            DESCRIPTION.
        see MassUnivariate.mass_univariate for full variable descriptions
        Returns
        -------
        new_df : TYPE
            DESCRIPTION.
        """
        disable_tqdm = kwargs.get('disable_tqdm',False)
        new_df = pd.DataFrame()
        if cont_independentVar_cols is None:
            cont_independentVar_cols = []
        for threshold in tqdm.tqdm(thresholds,disable=disable_tqdm):
            try:
                temp_model, temp_model_summary = cls.mass_univariate(
                    df,
                    cat_independentVar_cols=cat_independentVar_cols,
                    cont_independentVar_cols=cont_independentVar_cols + [threshold],
                    dependentVar_cols=dependentVar_cols,**kwargs)
                temp_model_summary.reset_index(drop=False, inplace=True)
                threshold_name = [i for i in temp_model.params.index if threshold in i][0]
                temp_model_summary.rename(
                    {
                        'index': 'Connection',
                        threshold_name + '_coef': f'{threshold_prefix}_coef',
                        threshold_name + '_pval': f'{threshold_prefix}_pval'
                    },
                    axis=1,
                    inplace=True)
            except UFuncTypeError:
                if isinstance(cont_independentVar_cols, np.ndarray):
                    threshold_array = df[threshold].values.reshape(-1,1)
                    updated_cont_independentVar_cols = np.hstack([cont_independentVar_cols,threshold_array])
                    temp_model, temp_model_summary = cls.mass_univariate(
                        df,
                        cat_independentVar_cols=cat_independentVar_cols,
                        cont_independentVar_cols=updated_cont_independentVar_cols,
                        dependentVar_cols=dependentVar_cols,**kwargs)
                    threshold_idx = updated_cont_independentVar_cols.shape[1]-1
                temp_model_summary.reset_index(drop=False, inplace=True)
                threshold_name = [i for i in temp_model.params.index if threshold in i][0]
                temp_model_summary.rename(
                    {
                        'index': 'Connection',
                        threshold_name + '_coef':f'{threshold_prefix}_coef',
                        threshold_name + '_pval': f'{threshold_prefix}_pval',
                        f'Cont_{threshold_idx}_coef':f'{threshold_prefix}_coef',
                        f'Cont_{threshold_idx}_pval':f'{threshold_prefix}_pval',
                    },
                    axis=1,
                    inplace=True)
            temp_model_summary['threshold'] = threshold
            new_df = pd.concat([new_df,temp_model_summary],axis=0)
    
        new_df.reset_index(drop=True, inplace=True)
        return new_df

    @classmethod
    def calculate_R_squared_explained(cls,df: pd.DataFrame,
                                      col_to_drop:List[str]=None,**kwargs) -> float:
        """[Calculate R squared explained from the model]

        Args:
            df ([pd.DataFrame]): [the model to be passed to the univariate model]
            col_to_drop (List[str], optional): [the column names of the data frame to be removed in the univariate model]. Defaults to None.
            **kwargs:
            cat_independentVar_cols (Optional[Union[List[str], List[np.ndarray]]], optional): [list of categorical variables, such that they will be converted to dummies by pandas]. Defaults to None.
            cont_independentVar_cols (Optional[Union[List[str], List[np.ndarray]]], optional): [list of continuous variables, they will be appended to cat_independentVar_cols]. Defaults to None.
            dependentVar_cols (Optional[Union[List[str], List[np.ndarray]]], optional): [the dependent variable, the ]. Defaults to None.
            scaling [str]: Default = both. ('x','y','both','none')
            If none, we will not perform standard scaler, 'both' we will perform on both x (independent variable- feature) and y (dependent variable- target)            col_to_drop [list[str]] = if we want to remove any column from the independent Variable before fitting the model.
            additional_info ([type], optional): [additional columns to be appended]. Defaults to None.
        Returns:
            [float]: [difference in the full and the null model R squared]
        
        """
        full_model, _ = cls.mass_univariate(df,**kwargs)
        if not col_to_drop:
            return full_model.rsquared
        null_model, _ = cls.mass_univariate(df,col_to_drop=col_to_drop, **kwargs)
        return full_model.rsquared - null_model.rsquared
    
    @classmethod
    def get_model_summary(cls,df:pd.DataFrame,
                              cat_independentVar_cols: Optional[List[str]] = None,
                              cont_independentVar_cols: Optional[List[str]] = None,
                              dependentVar_cols: Optional[List[str]] = None,
                              **kwargs):
        """
        Print model summary with Beta coefficient, Pvalues and R squared for an individual statsmodel

        Parameters
        ----------
        *same arguments as MassUnivariate.mass_univariate
        Returns
        -------
        result_df : pd.DataFrame
            DataFrame, index = independent Variable, columns = beta, p-value and Rsquared (fullmodel - null model)

        """
        #print model summary with beta, p-value and R2
        result_dict = defaultdict(list)
        if cat_independentVar_cols is None:
            cat_independentVar_cols = []
        if cont_independentVar_cols is None:
            cont_independentVar_cols = []
        full_model, _ = cls.mass_univariate(df,cat_independentVar_cols=cat_independentVar_cols,
                                            cont_independentVar_cols=cont_independentVar_cols,
                                            dependentVar_cols = dependentVar_cols,**kwargs)
        result_dict['beta_coefs'] = full_model.params.tolist()
        result_dict['pvalues'] = full_model.pvalues.tolist()
        for variable in full_model.params.index.tolist():
            result_dict['Rsquared'].append(
                cls.calculate_R_squared_explained(
                df,
                col_to_drop=variable,
                cat_independentVar_cols=cat_independentVar_cols,
                cont_independentVar_cols=cont_independentVar_cols,
                dependentVar_cols = dependentVar_cols)
                )
        result_df = pd.DataFrame(result_dict,index = full_model.params.index)
        return result_df
    
    @classmethod
    def check_all_predictors_combo_linear_Reg(cls,df: Optional[pd.DataFrame] = None,
                                            cat_independentVar_cols: Optional[List[str]] = None,
                                            cont_independentVar_cols: Optional[List[str]] = None,
                                            check_cols:Optional[List[str]]=None,
                                            check_plan:Optional[str]=None,
                                            dependentVar_cols: Optional[List[str]] = None,**kwargs):
        """[Perform univariate test on all combinations of predictors]

        Args:
            df (Optional[pd.DataFrame]): [description]
            cat_independentVar_cols (Optional[List[str]], optional): [categorical variable]. Defaults to None.
            cont_independentVar_cols (Optional[List[str]], optional): [Continuous variables]. Defaults to None.
            dependentVar_cols (Optional[List[str]], optional): [description]. Defaults to None.
        Returns:
            [type]: [description]
        """
        all_models = defaultdict(list)
        disable_tqdm = kwargs.get('disable_tqdm',False)
        def print_model_results(model: sm.regression.linear_model.RegressionResultsWrapper,
                                model_name: str,
                                dictionary: dict = all_models) -> None:
            #convenience function to print the model results from the sm.regression model
            
            variables = model.params.index.to_list()
            len_variables = len(variables)-1
            coefs = model.params.to_list()
            p_vals = model.pvalues.to_list()
            aic = model.aic
            R2 = model.rsquared
            R2_adj = model.rsquared_adj

            dictionary[model_name].append(
                [len_variables, variables, coefs, p_vals, aic, R2, R2_adj])
        
        null_model, _ = cls.mass_univariate(df=df,
                                        cat_independentVar_cols=None,
                                        cont_independentVar_cols=None,
                                        dependentVar_cols=dependentVar_cols)
        print_model_results(null_model, '0_0')
        if not cat_independentVar_cols:
            cat_independentVar_cols = []
        if not cont_independentVar_cols:
            cont_independentVar_cols = []
        total_predictors = cat_independentVar_cols + cont_independentVar_cols
        
        check_all=False
        if not check_cols:
            check_all=True
            check_cols = total_predictors
        
        if check_plan=='sequential':
            k_combo = (check_cols[0:n] for n in range(1,len(check_cols)+1))
            for idx,model_combo in tqdm.tqdm(enumerate(k_combo),disable=disable_tqdm):
                cat_independentVar_cols_temp = [i for i in cat_independentVar_cols if i not in check_cols]
                cont_independentVar_cols_temp = [i for i in cont_independentVar_cols if i not in check_cols]
                for _, covar in enumerate(model_combo):

                    if covar in cat_independentVar_cols:
                        cat_independentVar_cols_temp.append(covar)
                    elif covar in cont_independentVar_cols:
                        cont_independentVar_cols_temp.append(covar)
                if len(cat_independentVar_cols_temp) == 0:
                    cat_independentVar_cols_temp = None
                if len(cont_independentVar_cols_temp) == 0:
                    cont_independentVar_cols_temp = None
                
                model_temp, _ = cls.mass_univariate(df=df,
                                                cat_independentVar_cols=cat_independentVar_cols_temp,
                                                cont_independentVar_cols=cont_independentVar_cols_temp,
                                                dependentVar_cols=dependentVar_cols)

                model_name_temp = str(len(model_combo))+'_'+str(idx)
                print_model_results(model_temp, model_name_temp)
        # for k in range(1,len(total_predictors)+1):
        else:
            for k in tqdm.tqdm(range(1, len(check_cols)+1),disable=disable_tqdm):
                k_combo = combinations(check_cols, k)
                for idx, model_combo in enumerate(k_combo):
                    cat_independentVar_cols_temp = []
                    cont_independentVar_cols_temp = []
                    if not check_all:
                        cat_independentVar_cols_temp = [i for i in cat_independentVar_cols if i not in check_cols]
                        cont_independentVar_cols_temp = [i for i in cont_independentVar_cols if i not in check_cols]
                    for _, covar in enumerate(model_combo):
    
                        if covar in cat_independentVar_cols:
                            cat_independentVar_cols_temp.append(covar)
                        elif covar in cont_independentVar_cols:
                            cont_independentVar_cols_temp.append(covar)
                    if len(cat_independentVar_cols_temp) == 0:
                        cat_independentVar_cols_temp = None
                    if len(cont_independentVar_cols_temp) == 0:
                        cont_independentVar_cols_temp = None
                    
                    model_temp, _ = cls.mass_univariate(df=df,
                                                    cat_independentVar_cols=cat_independentVar_cols_temp,
                                                    cont_independentVar_cols=cont_independentVar_cols_temp,
                                                    dependentVar_cols=dependentVar_cols)
    
                    model_name_temp = str(k)+'_'+str(idx)
                    print_model_results(model_temp, model_name_temp)

        return all_models

    @classmethod
    def preprocess_forward_selection(cls,dictionary: dict) -> List[pd.DataFrame]:
        """[Preprocess the info of mass univariate tests, all possible combo of predictors
        Input is the output from ```check_all_predictors_combo_linear_Reg```]

        Args:
            dictionary (dict): [Output form ```check_all_predictors_combo_linear_Reg```]

        Returns:
            List[pd.DataFrame]: [4 data frames - score_summary, variable combo summary, beta coefs, p-values]
        """
        temp_df = pd.DataFrame(dictionary).T.reset_index(drop=True)
        temp_df = pd.concat([temp_df.drop(0, axis=1), temp_df[0].apply(
            pd.Series)], axis=1)  # this will preprocess the dictionary
        temp_df.columns = ['N_var', 'Var', 'Beta', 'P_val', 'AIC', 'R2', 'R2_adj']
        model_score_summary = temp_df[['N_var', 'AIC', 'R2', 'R2_adj']].copy()
        model_var_summary = temp_df[['Var']].copy()
        all_predictors = model_var_summary.iloc[-1, 0]
        label_binarizer = LabelBinarizer().fit(all_predictors)
        model_var_summary = pd.DataFrame(model_var_summary['Var'].apply(
            lambda x: label_binarizer.transform(x).sum(axis=0)))['Var'].apply(pd.Series)
        model_var_summary.columns = label_binarizer.classes_
        model_var_summary = model_var_summary[all_predictors]

        model_beta_summary = temp_df['Beta']
        model_p_summary = temp_df['P_val']
        model_beta = defaultdict(list)
        model_p = defaultdict(list)
        for idx in range(len(model_var_summary)):
            beta_iter = iter(model_beta_summary.iloc[idx])
            p_iter = iter(model_p_summary.iloc[idx])
            for n in model_var_summary.iloc[idx]:
                if n == 1:
                    model_beta[idx].append(next(beta_iter))
                    model_p[idx].append(next(p_iter))
                else:
                    model_beta[idx].append(np.nan)
                    model_p[idx].append(np.nan)
        model_beta_summary = pd.DataFrame(model_beta).T
        model_p_summary = pd.DataFrame(model_p).T
        model_beta_summary.columns = model_var_summary.columns
        model_p_summary.columns = model_var_summary.columns

        return model_score_summary, model_var_summary, model_beta_summary, model_p_summary

    @classmethod
    def print_summary_table(cls,
                            df:pd.DataFrame,
                            thresholds:List[str]=None,
                            cat_independentVar_cols:List[str]=None,
                            cont_independentVar_cols:List[str]=None,
                            dependentVar_cols:List[str]=None,
                            **kwargs)->pd.DataFrame:
        """
        

        Parameters
        ----------
        see data_exploration.MassUnivariate.mass_univariate for full description of the variables
        Returns
        -------
        summary_table : pd.DataFrame
            The summary table containing R, Beta value, P-value for each dependent variable at each PRS threshold.

        """
        disable_tqdm = kwargs.get('disable_tqdm',False)

        Result_dict=defaultdict(dict)
        for dependent_variable in tqdm.tqdm(dependentVar_cols,disable=disable_tqdm):
            Result_dict[dependent_variable] = defaultdict(dict)
            for threshold in thresholds:
                Result_dict[dependent_variable][threshold] = defaultdict(dict)
                Result_dict[dependent_variable][threshold]['R2'] = defaultdict(dict)
                temp_model, _ = cls.mass_univariate(
                    df=df,
                    cat_independentVar_cols=cat_independentVar_cols,
                    cont_independentVar_cols=cont_independentVar_cols + [threshold],
                    dependentVar_cols=[dependent_variable]) # calculate a full model
                Result_dict[dependent_variable][threshold]['Beta'] = temp_model.params[1:].to_dict()
                Result_dict[dependent_variable][threshold]['P_val'] = temp_model.pvalues[1:].to_dict()
                for col_to_drop in cont_independentVar_cols + cat_independentVar_cols + [threshold]:
                    Result_dict[dependent_variable][threshold]['R2'][
                        col_to_drop] = cls.calculate_R_squared_explained(
                            df=df,
                            col_to_drop=col_to_drop,
                            cat_independentVar_cols=cat_independentVar_cols,
                            cont_independentVar_cols=cont_independentVar_cols+[threshold],
                            dependentVar_cols=[dependent_variable])
        
        summary_table = pd.DataFrame.from_dict({(i,j,k): Result_dict[i][j][k] 
                                                for i in Result_dict.keys() 
                                                for j in Result_dict[i].keys() 
                                                for k in Result_dict[i][j].keys()},
                       orient='index')
        
        return summary_table

class MultipleCorrection:
    @staticmethod
    def fdr(df:pd.DataFrame=None,
            p_val:Union[np.ndarray,str]=None,
            alpha:float=0.05,
            return_adj:bool=True):
        if isinstance(df,pd.DataFrame):
            if not isinstance(p_val,str):
                return TypeError('Must give the column name if providing dataframe')
            p_val = df[p_val].values
        elif isinstance(p_val,np.ndarray):
            if p_val.ndim != 1:
                p_val = p_val.reshape(-1)
        survived,adjusted_pval = fdrcorrection(p_val)
        if isinstance(df,pd.DataFrame):
            if return_adj:
                df['adjP'] = adjusted_pval
            return df[survived]
        else:
            return survived,adjusted_pval
            
            

    @staticmethod
    def matSpDLite(correlation_matrix:np.ndarray,alpha:str = 0.05):
        """
        Adapted from Nyholt DR R script.
        Please cite
        Nyholt DR (2004) A simple correction for multiple testing for SNPs in linkage disequilibrium with each other. Am J Hum Genet 74(4):765-769.
        and 
        http://gump.qimr.edu.au/general/daleN/matSpDlite/
        and
        Li and Ji 2005. 
        
        Parameters
        ----------
        correlation_matrix : np.ndarray
            The correlation matrix. It must be symmetric.
        alpha : str, optional
            DESCRIPTION. The default is 0.05.

        """
        evals,_ = np.linalg.eigh(correlation_matrix.T)
        evals = np.sort(evals)[::-1]
        
        oldV = np.var(evals,ddof=1)
        M = len(evals)
        L = M-1
        Meffold = (L*(1- oldV/M)) + 1
        
        print(f'Effective Number of Independent Variables [Veff] is {Meffold}')
        newevals = np.where(evals<0,0,evals) # negative eigenvalues are set to 0
        
        IntLinewevals = np.where(newevals>=1,1,0) #the integral part "represents identical tests that should be counted as one in Meff"
        NonIntLinewevals = newevals - np.floor(newevals) # the non integral part should represent the partially correlated test that should be counted as a fractional number between 0 and 1
        MeffLi = np.sum(IntLinewevals + NonIntLinewevals)
        
        print(f'Effective Number of Independent Variables [VeffLi] (Using equation 5 of Li and Ji 2005) is {np.round(MeffLi)}')
        
        if MeffLi < Meffold:
            adjusted_p_val = alpha/MeffLi
        else:
            adjusted_p_val = alpha/Meffold
        print(f'The adjusted multiple testing correction p-val is alpha/lower(Meff) = {adjusted_p_val}')
        return MeffLi


# def save_dict_with_pickle(dictionary: Optional[dict],
#                           file_path: Optional[str]) -> None:
#     a_file = open(file_path, 'wb')
#     pickle.dump(dictionary, a_file)
#     a_file.close()


# def open_dict_with_pickle(file_path: Optional[str]) -> dict:
#     a_file = open(file_path, 'rb')
#     dictionary = pickle.load(a_file)
#     return dictionary

def perform_CCA(X,Y,scale=True):
    if scale:
        X = StandardScaler().fit_transform(X)
        Y = StandardScaler().fit_transform(Y)
    
    stats_cca = CanCorr(X, Y)
    return stats_cca.corr_test().summary()

class Stability_tests:
    
    @staticmethod
    
    def train_test_split_modified(df: Union[pd.DataFrame, np.ndarray] = None,*stratify_by_args, bins : int =4,
                                  test_size: float = 0.5, random_state: int = 42) -> tuple:
        """[splitting the data based on several stratification]
    
        Args:
            df (Union[pd.DataFrame, np.ndarray], optional): [the data/ dataframe to be split]. Defaults to None.
            bins (int, optional): [the bins used to separate the continuous data,
                                        if it is too high, then due to small dataset, there might be error due to not enough data in each class]. Defaults to 4.
            This works by concatenate multiple stratification criteria together, and then attempt train test split. This is done at each level of stratification. If the stratification is not successful, we reduce the bins number, and try again.
            This is done in succession, so depending on what you want to stratify by, you put it earlier in the list. so GA_vol, PMA_vol will stratify first by GA, and then PMA.
        Returns:
            tuple : train and test set.
        """
        def attempting_train_test_split(df, stratify_by, idx, test_size,random_state):
            try:
                train, test = train_test_split(df, stratify=stratify_by, test_size=test_size, random_state=random_state)
                return train, test
            except ValueError:
                stratification_list.pop()  # remove the last iteration
                print('changing bins for %d argument' % idx)
    
        input_bins = bins
        stratification_list = []
        for idx, stratification in enumerate(stratify_by_args):
            bins = input_bins
            while True:
                if isinstance(stratification, str):
                    strat = df.loc[:, stratification].values
                    if isinstance(strat[0], float):
                        strat = pd.cut(strat, bins=bins, labels=False)
                elif isinstance(stratification, np.ndarray):
                    strat = stratification
                    if isinstance(stratification[0], float):
                        strat = pd.cut(strat, bins=bins, labels=False)
                stratification_list.append(strat)
                stratify_by = [''.join(map(lambda x: str(x), i))
                               for i in zip(*stratification_list)]
                train_test = attempting_train_test_split(df, stratify_by, idx,test_size=test_size,random_state=random_state)
                if train_test:
                    break
                else:
                    bins -= 1

        return train_test
    
    @staticmethod
    def split_group(df:Union[pd.DataFrame, np.ndarray],
                    stratify_by_args:Union[str,np.array]=None,
                    n=2,
                    fraction:Union[List[float],float]=None,
                    bins:int=4):
        """Splitting dataframe or array into groups

        Args:
            df (Union[pd.DataFrame, np.ndarray]): DataFrame or Array
            stratify_by_args (Union[str,np.array], optional): list of string or columns names that need to be stratified. Defaults to None.
            n (int, optional): number of groups. Defaults to 2.
            bins (int, optional): bins to stratify the continuous variables. Defaults to 4.

        Returns:
            List[pd.DataFrame]: list of dataframe corresponding for each group
        """
        if isinstance(df,np.ndarray):
            temp_df = pd.DataFrame(df)
        elif isinstance(df,pd.DataFrame):
            temp_df = df.copy()
        
        
        stratification_list = []
        if stratify_by_args is not None:
            for idx, stratification in enumerate(stratify_by_args):
                if isinstance(stratification, str):
                    strat = df.loc[:, stratification].values
                    if isinstance(strat[0], float):
                        strat = pd.cut(strat, bins=bins, labels=False)
                elif isinstance(stratification, np.ndarray):
                    strat = stratification
                    if isinstance(stratification[0], float):
                        strat = pd.cut(strat, bins=bins, labels=False)
                stratification_list.append(strat)
                stratify_by = [''.join(map(lambda x: str(x), i))
                                for i in zip(*stratification_list)]
                
            temp_df['stratify_by'] = stratify_by
            unique_stratified_group = np.unique(stratify_by)
            if isinstance(fraction,float):
                return df.iloc[temp_df.groupby('stratify_by',group_keys=False).apply(lambda x: x.sample(frac=fraction)).index]
            all_group = pd.concat([
                temp_df[temp_df['stratify_by']==unique_group].apply(
                    lambda x: np.random.choice([
                        i for i in range(n)],1)[0],axis=1) for unique_group in unique_stratified_group
                ])
        else:
            if isinstance(fraction,float):
                return df.iloc[temp_df.sample(frac=fraction).index]
            all_group = temp_df.apply(
                lambda x: np.random.choice([i for i in range(n)],1)[0],axis=1)
            
        return [temp_df.iloc[all_group[all_group==i].index] for i in range(n)]
        
        
    
    
    # @staticmethod
    # def generate_stratified_fold(df: Union[pd.DataFrame, np.ndarray] = None,
    #                               *stratify_by_args, 
    #                               bins : int =4,
    #                               n_splits=3,
    #                               random_state: int = 42):
    #     stratified_split = StratifiedKFold(n_splits=n_splits)
    #     stratification_list = []
    #     for idx, stratification in enumerate(stratify_by_args):
    #         bins = input_bins
    #         while True:
    #             if isinstance(stratification, str):
    #                 strat = df.loc[:, stratification].values
    #                 if isinstance(strat[0], float):
    #                     strat = pd.cut(strat, bins=bins, labels=False)
    #             elif isinstance(stratification, np.ndarray):
    #                 strat = stratification
    #                 if isinstance(stratification[0], float):
    #                     strat = pd.cut(strat, bins=bins, labels=False)
    #             stratification_list.append(strat)
    #             stratify_by = [''.join(map(lambda x: str(x), i))
    #                             for i in zip(*stratification_list)]
    #             try:
    #                 train, test = stratified_split.split(df,stratify_by)
    #                 return train, test
    #             except ValueError:
    #                 stratification_list.pop()  # remove the last iteration
    #                 print('changing bins for %d argument' % idx)
            
            
        
        
        
    @staticmethod
    def divide_high_low_risk(y: Optional[np.ndarray], high_perc: float = 0.1, low_perc: float = 0.3) -> List[np.ndarray]:
        """[Divide the dataset into top and bottom x%. Here, we take the assumption that top percent is high risk and bottom percent is low risk.
            While this method maximises the odd ratio for impacts, it raises concerns about the arbitrariness of the quantile used]
    
        Args:
            y (Optional[np.ndarray]): [the raw PRS score]
            high_perc (float, optional): [higher risk group percentage]. Defaults to 0.1.
            low_perc (float, optional): [lower risk group percentage]. Defaults to 0.3.
    
        Raises:
            Exception: [If high risk + low risk > total subject, raise exception]
    
        Returns:
            Union[np.ndarray]: [list of indices]
            high_risk_indices, low_risk_indices
        """
        high_risk_number = int(np.ceil(high_perc*len(y)))
        low_risk_number = int(np.ceil(low_perc*len(y)))
        if high_risk_number+low_risk_number > len(y):
            raise Exception('The high and low risk selection overlapped')
        # bottom
        if isinstance(y,pd.Series):
            y = y.values
        low_risk = np.argsort(y)[:low_risk_number]
        # top
        high_risk = np.argsort(y)[::-1][:high_risk_number]
    
        return high_risk, low_risk
    
    
    @staticmethod
    def perform_t_test(group_1: np.ndarray,
                       group_2: np.ndarray) -> List[float]:
        """[perform t-test]
    
        Args:
            group_1 (np.ndarray): [The arrays must have the same shape, except in the dimension corresponding to axis]
            group_2 (np.ndarray):
    
        Returns:
            List[float]: [stats,pval]
        """
        stats, pval = ttest_ind(group_1, group_2, equal_var=True)
        return stats, pval

    @staticmethod

    def nn_matching(df: Optional[pd.DataFrame] = None,
                    cat_independentVar_cols: Union[List[str],
                                                     np.ndarray,
                                                     pd.DataFrame,
                                                     pd.Series] = None,
                    cont_independentVar_cols: Union[List[str],
                                                     np.ndarray,
                                                     pd.DataFrame,
                                                     pd.Series] = None,
                    dependentVar_cols: Union[List[str],
                                                     np.ndarray,
                                                     pd.DataFrame,
                                                     pd.Series] = None,
                    scaling: str='x',
                    random_state:int=None,
                    order:str='random',
                    threshold:float=None,
                    **kwargs) ->pd.DataFrame:
        """
        Nearest neighbour without replacement pair matching
        Generate propensity score for each subject and then pair them using nearest neighbour algorithm
        Propensity score is just the probability of group assignment condiational
            on observed baseline covariates
        idea based on this paper : https://onlinelibrary.wiley.com/doi/10.1002/sim.6004
        Parameters
        ----------
        df : Optional[pd.DataFrame], optional
            data frame already preprocessed to have only 2 groups. The default is None.
        cat_independentVar_cols : Union[List[str],np.ndarray,pd.DataFrame,pd.Series], optional
            categorical variable to stratify on. The default is None.
        cont_independentVar_cols : Union[List[str],np.ndarray,pd.DataFrame,pd.Series], optional
            continuous variable to stratify on. The default is None.
        dependentVar_cols : Union[List[str],np.ndarray,pd.DataFrame,pd.Series], optional
            single column from where the category are from. The default is None.
        scaling : str, optional
            whether to standardise. The default is 'x'.
        random_state : int, optional
            randomise the nearest neighbour search. The default is None.
        order: str, optional
            {'random','ascending'} if random, the nearest neighbour will be randomly initialised.
                if ascending, then the propensity score will be ordered, so the lowest ones
                will find the matching first.
        threshold : float, optional
            the threshold below which the nearest neighbour distance is evaluated. The default is None.
        -------
        pd.DataFrame
            data frame for group 1
        pd.DataFrame
            data frame for group 2

        """
         
        X_cat, X_cont, groups = MassUnivariate.prepare_data(df = df,
                            cat_independentVar_cols = cat_independentVar_cols,
                            cont_independentVar_cols = cont_independentVar_cols,
                            dependentVar_cols = dependentVar_cols,return_type='dataframe',**kwargs)
        if scaling == 'x':
            if not X_cont.empty:
                X_cont = StandardScaler().fit_transform(X_cont)
        X = pd.concat([X_cat,X_cont],axis=1)
        y = groups.values.reshape(-1)
        if len(np.unique(groups)) != 2:
            raise ValueError('need exactly 2 groups')
        if isinstance(threshold,float):
            if not(0<threshold<1):
                raise ValueError('threshold must be between 0 and 1')
        if isinstance(dependentVar_cols,list):
            if len(dependentVar_cols) > 1:
                raise ValueError('can match by 1 category')
            dependentVar_cols = dependentVar_cols[0]
        #fit logistic regression to get propensity score (i.e., probability of being one class)
        log_reg = LogisticRegression().fit(X,y)
        propensity = log_reg.predict_proba(X)[:,1] # predicting the larger group?
        groups['propensity'] = propensity
        
        g1 = groups.loc[groups[dependentVar_cols]==np.unique(y)[0],'propensity']
        g2 = groups.loc[groups[dependentVar_cols]==np.unique(y)[1],'propensity']
        
        if len(g1) > len(g2): #make sure that the first group is smaller one
            g1, g2 = g2, g1
        
        if order == 'random':
            g1 = g1.sample(frac = 1,random_state=random_state) # permute the rows, start from random point
        if order == 'ascending':
            g1 = g1.sort_values(ascending=True)
        g1_retain = []
        g2_retain = []
        for idx in g1.index:
            distance = abs(g1.loc[idx] - g2)
            if isinstance(threshold,float):
                if distance.min() <= threshold:
                    g1_retain.append(idx)
                    g2_retain.append(distance.index[distance.argmin()])
                    g2 = g2.drop(distance.index[distance.argmin()])
                    #what to do with the ones that do not have match?
            else:
                g1_retain.append(idx)
                g2_retain.append(distance.index[distance.argmin()])
                g2 = g2.drop(distance.index[distance.argmin()])
        
        return df.iloc[g1_retain], df.iloc[g2_retain]
        
class FeatureReduction:
    
    @staticmethod
    def retain_non_zero_features(df:pd.DataFrame,
                                 dependentVar_cols:Optional[Union[List[str],
                                                 List[np.ndarray]]] = None,
                                 threshold:float=0.5)->pd.DataFrame:
        """
        Retain non zero features
        Features that contain more than x number of 0 observation is removed.
        x is set as threshold.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame need to be reduced.
        dependentVar_cols : Optional[Union[List[str] List[np.ndarray]]], optional
            List of features need to be reduced. The default is None.
        threshold : float, optional
            Features that contained > threshold number of 0 observation
            is removed. The default is 0.5.

        Returns
        -------
        pd.DataFrame
            Reduced features dataframe.

        """
        zero_perc_calc=lambda feature: np.sum(feature==0)/len(feature)
        dependentVars = df.loc[:,dependentVar_cols].copy()
        cols_to_drop = dependentVars.columns[dependentVars.apply(zero_perc_calc)>threshold]
        return df.drop(columns=cols_to_drop)
    
    
    @staticmethod
    def perform_PCA(df:Union[pd.DataFrame,np.ndarray],
                    dependentVar_cols:Optional[List[str]] = None,
                    n_components:int=None,
                    random_state:int=42,
                    scaling:bool=True):
        """
        Perform PCA

        Parameters
        ----------
        df : Union[pd.DataFrame,np.ndarray]
            DataFrame need to be feature reduced.
        dependentVar_cols : Optional[List[str]], optional
            List of feature names need to be reduced. The default is None.
        n_components : int, optional
            number of components to be retained. The default is None.
        random_state : int, optional
            passed to PCA sklearn. The default is 42.
        scaling : bool, optional
            apply StandardStandardize to the features. The default is True.
            sklearn PCA doesn't automatically do it. It only substract the mean.

        Returns
        -------
        pca : sklearn.pca
            sklearn pca model.
        X_pca : np.ndarray
            Returned PCs.
        loading_matrix : pd.DataFrame
            contribution (corr matrix) between each variable to the PC.

        """
        pca = PCA(n_components=n_components,
                  random_state=random_state)
        if dependentVar_cols is not None:
            if not isinstance(dependentVar_cols,list):
                dependentVar_cols = [dependentVar_cols]
        if isinstance(df,pd.DataFrame):
            if dependentVar_cols is None:
                X = df.to_numpy()
            else:
                X = df[dependentVar_cols].to_numpy()
        elif isinstance(df,np.ndarray):
            X = df.copy()
        if scaling:
            X = StandardScaler().fit_transform(X)
        X_pca = pca.fit_transform(X)
        loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
        if dependentVar_cols is not None:
            loading_matrix = pd.DataFrame(loadings, index = dependentVar_cols)
        else:
            loading_matrix = pd.DataFrame(loadings)
        return pca, X_pca, loading_matrix    
    
    @staticmethod
    def combine_columns_together(df:pd.DataFrame,
                                 group_columns:Union[dict,List],
                                 operation:str = 'sum',
                                 remove_duplicated:bool=True):
        """
        Combine the columns by performing an operation on it.

        Parameters
        ----------
        df : pd.DataFrame
            Data Frame of interest.
        group_columns_dict : dict
            Dictionary {'new grouped name': [ list of columns names need to be grouped]}.
            new grouped name cannot be the same name as the original names
        operation : str, optional
            {'sum','mean'}. The default is 'sum
        remove_duplicated : bool, optional
            If you don't want to use the new grouped name, but only update the original columns. The default is True.
            if passing list, then drop the columns
            Useful when you want to plot

        Returns
        -------
        temp_df : pd.DataFrame
            New updated df

        """
        temp_df = df.copy()
        if isinstance(group_columns, dict):
            for group,column_names in group_columns.items():
                if operation == 'sum':
                    temp_df[group] = temp_df[column_names].sum(axis=1)
                elif operation == 'mean':
                    temp_df[group] = temp_df[column_names].mean(axis=1)
                if remove_duplicated:
                    temp_df.drop(columns = column_names,inplace=True)
                else:
                    for column in column_names:
                        temp_df[column] = temp_df[group]
                    temp_df.drop(columns = group, inplace=True)
        elif isinstance(group_columns,list):
            if not isinstance(group_columns[0],list):
                raise AttributeError('pass list of list if have only 1 group')
            for column_names in group_columns:
                if operation == 'sum':
                    temp_df['temp'] = temp_df[column_names].sum(axis=1)
                elif operation == 'mean':
                    temp_df['temp'] = temp_df[column_names].mean(axis=1)
                for column in column_names:
                    temp_df[column] = temp_df['temp']
                temp_df.drop(columns = 'temp', inplace=True)
                if remove_duplicated:
                    temp_df.drop(columns=column_names[1:],inplace=True)
        return temp_df
