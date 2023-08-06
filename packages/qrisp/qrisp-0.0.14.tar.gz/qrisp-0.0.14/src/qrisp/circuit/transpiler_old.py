"""
/*********************************************************************
* Copyright (c) 2023 the Qrisp Authors
*
* This program and the accompanying materials are made
* available under the terms of the Eclipse Public License 2.0
* which is available at https://www.eclipse.org/legal/epl-2.0/
*
* SPDX-License-Identifier: EPL-2.0
**********************************************************************/
"""

# -*- coding: utf-8 -*-


import numpy as np
from qrisp.circuit.operation import PTControlledOperation, ControlledOperation

#This function dissolves any Operation objects that have a definition circuit such that the result only consists of elementary gates
def transpile(qc, transpilation_level = np.inf, transpile_predicate = None, **kwargs):
    
    from qrisp.circuit import Operation, QuantumCircuit, Qubit, Clbit
    QuantumCircuit.fast_append = True
    from qrisp.circuit import Qubit, Clbit
    transpiled_qc = QuantumCircuit()
    
    # [transpiled_qc.add_qubit(Qubit(qb.identifier)) for qb in qc.qubits]
    # [transpiled_qc.add_clbit(Clbit(cb.identifier)) for cb in qc.clbits]
    
    for qb in qc.qubits:
        if isinstance(qb, Qubit):
            transpiled_qc.add_qubit(qb)
        else:
            transpiled_qc.add_qubit(Qubit(qb.identifier))
            
    for cb in qc.clbits:
        if isinstance(qb, Qubit):
            transpiled_qc.add_clbit(cb)
        else:
            transpiled_qc.add_clbit(Clbit(cb.identifier))
    
    for i in range(len(qc.data)):
        
        instruction = qc.data[i]
        
        if instruction.op.definition == None or transpilation_level <= 0:
            transpiled_qc.data.append(instruction)
        else:
            
            if transpile_predicate:
                if not transpile_predicate(instruction.op):
                    transpiled_qc.data.append(instruction)
                    continue
                
            definition_qc = transpile(instruction.op.definition, transpilation_level = transpilation_level -1, transpile_predicate = transpile_predicate).copy()
            
            
            translation_dic = {}
            
            translation_dic.update({definition_qc.qubits[j].identifier : instruction.qubits[j] for j in range(instruction.op.num_qubits)})
            translation_dic.update({definition_qc.clbits[j].identifier : instruction.clbits[j] for j in range(instruction.op.num_clbits)})
            
            extend(transpiled_qc, definition_qc, translation_dic)
    
    QuantumCircuit.fast_append = False
    
    
    if not kwargs or not hasattr(qc, "to_qiskit"):
        return transpiled_qc
    else:
        from qrisp import QuantumCircuit
        qiskit_qc = transpiled_qc.to_qiskit()
        
        from qiskit import transpile as qiskit_transpile
        
        transpiled_qiskit_qc = qiskit_transpile(qiskit_qc, **kwargs)
        
        qrisp_qc = QuantumCircuit.from_qiskit(transpiled_qiskit_qc)
        
        return qrisp_qc



    


def extend(qc_0, qc_1, translation_dic = "id"):
    
    if translation_dic == "id":
        
        translation_dic = {}
        for qb in qc_1.qubits:
            translation_dic[qb] = qb
            if not qb in qc_0.qubits:
                qc_0.add_qubit(qb)
            
        for cb in qc_1.clbits:
            translation_dic[qb] = qb
            if not cb in qc_0.clbits:
                qc_0.add_clbit(cb)
            

    #Copy in order to prevent modification
    translation_dic = dict(translation_dic)

    for key in list(translation_dic.keys()):
        
        if not isinstance(key, str):
            translation_dic[key.identifier] = translation_dic[key]


    for i in range(len(qc_1.data)):
        
        instruction_other = qc_1.data[i]
        qubits = []
        for qb in instruction_other.qubits:
            qubits.append(translation_dic[qb.identifier])
        
        clbits = []
        
        for cb in instruction_other.clbits:
            clbits.append(translation_dic[cb.identifier])
        
        instr_type = type(instruction_other)
        
        qc_0.data.append(instr_type(instruction_other.op, qubits, clbits))
        